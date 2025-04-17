package com.github.trungdung1711.alert_delivery_service.event;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Alert {
	private String user_id;
	private String env_id;
	private String sensor_id;
	private String timestamp;
	private String type;
	private double max;
	private double min;
	private double value;
	private String mail;
}
