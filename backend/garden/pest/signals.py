import os
import base64
import cloudinary.uploader
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PlantImage
from inference_sdk import InferenceHTTPClient
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()


@receiver(post_save, sender=PlantImage)
def run_roboflow_inference(sender, instance, created, **kwargs):
    if created and instance.image:
        client = InferenceHTTPClient(
            api_url=os.getenv('MODEL_API_URL'),
            api_key=os.getenv('MODEL_API_KEY'),
        )

        result = client.run_workflow(
            workspace_name=os.getenv('MODEL_WORKSPACE'),
            workflow_id=os.getenv('MODEL_WORKFLOW'),
            images={'image': instance.image.url},
            use_cache=True,
        )

        base64_image = result[0].get('output_image')
        decoded_image = base64.b64decode(base64_image)
        
        del result[0]['output_image']
        predictions = result[0].get('predictions').get('predictions')
        
        upload_result = cloudinary.uploader.upload(
            BytesIO(decoded_image),
            folder='annotated_plant_images',
            overwrite=True,
            resource_type='image',
        )

        instance.annotated_image = upload_result['public_id']
        instance.predictions = predictions
        instance.save(update_fields=['annotated_image', 'predictions'])
