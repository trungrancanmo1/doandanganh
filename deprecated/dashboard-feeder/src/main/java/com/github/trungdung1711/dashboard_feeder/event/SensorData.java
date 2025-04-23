package com.github.trungdung1711.dashboard_feeder.event;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class SensorData {
	private String user_id;
	private String env_id;
	private String sensor_id;
	private String timestamp;
	private String type;
	private double value;
	private int state;
}