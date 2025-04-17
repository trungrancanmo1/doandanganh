package com.github.trungdung1711.threshold_validation_demo.event;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
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
