from utils import *
import base64
import cloudinary.uploader
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PlantImage
from inference_sdk import InferenceHTTPClient
from io import BytesIO
from django.conf import settings


@receiver(post_save, sender=PlantImage)
def run_roboflow_inference(sender, instance, created, **kwargs):
    if created and instance.image:
        client = InferenceHTTPClient(
            api_url=settings.OBJDET_API_URL,
            api_key=settings.OBJDET_API_KEY,
        )

        result = client.run_workflow(
            workspace_name=settings.OBJDET_WORKSPACE,
            workflow_id=settings.OBJDET_WORKFLOW,
            images={'image': instance.image.url},
            use_cache=True,
        )

        base64_image = result[0].get('output_image')
        decoded_image = base64.b64decode(base64_image)
        
        del result[0]['output_image']
        predictions = result[0].get('predictions').get('predictions')
        _send_inference_to_kafka_feed(str(instance.id), predictions)
        
        upload_result = cloudinary.uploader.upload(
            BytesIO(decoded_image),
            folder='annotated_plant_images',
            overwrite=True,
            resource_type='image',
        )

        instance.annotated_image = upload_result['public_id']
        instance.predictions = predictions
        instance.save(update_fields=['annotated_image', 'predictions'])


def _send_inference_to_kafka_feed(key, predictions):
    if not predictions:
        return
    
    kafka_producer.send(
        topic='ai-alert',
        key=key,
        value=json.dumps(predictions),
    )