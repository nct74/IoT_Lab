using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using M2MqttUnity;
using Newtonsoft.Json.Linq;
using System.Linq;
using Newtonsoft.Json;

namespace ChuongGa
{
	public class Status_Data
	{
		public string temperature { get; set; }
		public string humidity { get; set; }
	}

	public class Status_Device
	{
		public string device { get; set; }
		public string status { get; set; }
	}
	public class data_ss
	{
		public string ss_name { get; set; }
		public string ss_unit { get; set; }
		public string ss_value { get; set; }
	}

	public class Config_Data
	{
		public float temperature_max { get; set; }
		public float temperature_min { get; set; }
		public int mode_fan_auto { get; set; }
	}

	public class ControlFan_Data
	{
		public int fan_status { get; set; }
		public int device_status { get; set; }

	}

	public class ChuongGaMqtt : M2MqttUnityClient
	{
		public List<string> topics = new List<string>();


		public string msg_received_from_topic_status = "";
		public string msg_received_from_topic_control = "";


		private List<string> eventMessages = new List<string>();

		[SerializeField]
		public Config_Data _config_data;
		[SerializeField]
		public ControlFan_Data _controlFan_data;
		//============================================================================
		// Subcrise data from server
		public Text[] text_display = new Text[2];

		//============================================================================
		//Login - Connect to Server
		[SerializeField]
		public InputField brokerURL;
		[SerializeField]
		public InputField username;
		[SerializeField]
		public InputField password;

		//============================================================================
		// Update gia tri ban dau cua led va pump
		public SwitchButton led;
		public SwitchButton pump;


		//============================================================================
		// Public Data
		public void FirstPublicPump()
		{
			string data = "{\"device\": \"PUMP\",\"status\": \"OFF\"}";
			client.Publish("/bkiot/1915144/pump", System.Text.Encoding.UTF8.GetBytes(data), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
			Debug.Log("First public pump data");
		}
		public void FirstPublicLed()
		{
			string data = "{\"device\": \"LED\",\"status\": \"OFF\"}";
			client.Publish("/bkiot/1915144/led", System.Text.Encoding.UTF8.GetBytes(data), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
			Debug.Log("First public led data");
		}
		public void FirstPublicStatus()
		{
			string data = "{\"temperature\": 29,\"humidity\": 48}";
			client.Publish("/bkiot/1915144/status", System.Text.Encoding.UTF8.GetBytes(data), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
			Debug.Log("First public led data");
		}
		public void Connect_Server()
		{
			this.brokerAddress = brokerURL.text;
			this.mqttUserName = username.text;
			this.mqttPassword = password.text;
			// Start();
			Connect();
			// Debug.Log("Connected Complete");
		}
		// public void PublishConfig()
		// {
		// 	_config_data = new Config_Data();
		// 	GetComponent<ChuongGaManager>().Update_Config_Value(_config_data);
		// 	string msg_config = JsonConvert.SerializeObject(_config_data);
		// 	client.Publish(topics[1], System.Text.Encoding.UTF8.GetBytes(msg_config), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
		// 	Debug.Log("publish config");
		// }

		// public void PublishFan()
		// {
		// 	_controlFan_data = GetComponent<ChuongGaManager>().Update_ControlFan_Value(_controlFan_data);
		// 	string msg_config = JsonConvert.SerializeObject(_controlFan_data);
		// 	client.Publish(topics[2], System.Text.Encoding.UTF8.GetBytes(msg_config), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
		// 	Debug.Log("publish fan");
		// }

		public void SetEncrypted(bool isEncrypted)
		{
			this.isEncrypted = isEncrypted;
		}


		protected override void OnConnecting()
		{
			base.OnConnecting();
			//SetUiMessage("Connecting to broker on " + brokerAddress + ":" + brokerPort.ToString() + "...\n");
		}

		// protected override void OnConnected()
		// {
		// 	base.OnConnected();

		// 	// SubscribeTopics();
		// 	// This is place for first call to public data led && pump && data (temp, humi)
		// 	// this.FirstPublicLed();
		// 	// this.FirstPublicPump();
		// 	// this.FirstPublicStatus();
		// }

		protected override void SubscribeTopics()
		{

			foreach (string topic in topics)
			{
				if (topic != "")
				{
					client.Subscribe(new string[] { topic }, new byte[] { MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE });

				}
			}
		}

		protected override void UnsubscribeTopics()
		{
			foreach (string topic in topics)
			{
				if (topic != "")
				{
					client.Unsubscribe(new string[] { topic });
				}
			}

		}

		protected override void OnConnectionFailed(string errorMessage)
		{
			Debug.Log("CONNECTION FAILED! " + errorMessage);
		}

		protected override void OnDisconnected()
		{
			Debug.Log("Disconnected.");
		}

		protected override void OnConnectionLost()
		{
			Debug.Log("CONNECTION LOST!");
		}



		// protected override void Start()
		// {

		// 	base.Start();
		// }

		protected override void DecodeMessage(string topic, byte[] message)
		{
			string msg = System.Text.Encoding.UTF8.GetString(message);
			// Debug.Log("Received: " + msg);
			// StoreMessage(msg);
			if (topic == topics[0])
				ProcessMessageStatus(msg);

			if (topic == topics[1])
				ProcessMessageLed(msg);

			if (topic == topics[2])
				ProcessMessagePump(msg);
		}

		private void ProcessMessageStatus(string msg)
		{
			Status_Data _status_data = JsonConvert.DeserializeObject<Status_Data>(msg);
			// msg_received_from_topic_status = msg;
			// GetComponent<ChuongGaManager>().Update_Status(_status_data);
			text_display[0].text = (_status_data.temperature) + "°C";
			text_display[1].text = (_status_data.humidity) + "%";

		}

		private void ProcessMessageLed(string msg)
		{
			// _controlFan_data = JsonConvert.DeserializeObject<ControlFan_Data>(msg);
			// msg_received_from_topic_control = msg;
			// GetComponent<ChuongGaManager>().Update_Control(_controlFan_data);
			Status_Device _status_deivce = JsonConvert.DeserializeObject<Status_Device>(msg);
			// Debug.Log(_status_deivce.status);
			if (_status_deivce.status == "OFF")
				led.SetStatus(false);
			else if (_status_deivce.status == "ON")
				led.SetStatus(true);
		}
		private void ProcessMessagePump(string msg)
		{
			// _controlFan_data = JsonConvert.DeserializeObject<ControlFan_Data>(msg);
			// msg_received_from_topic_control = msg;
			// GetComponent<ChuongGaManager>().Update_Control(_controlFan_data);
			Status_Device _status_deivce = JsonConvert.DeserializeObject<Status_Device>(msg);
			// Debug.Log(_status_deivce.status);
			if (_status_deivce.status == "OFF")
				pump.SetStatus(false);
			else if (_status_deivce.status == "ON")
				pump.SetStatus(true);
		}

		public void switchButtonLed()
		{
			if (led.switchState == true)
			{
				string data = "{\"device\": \"LED\",\"status\": \"OFF\"}";
				client.Publish("/bkiot/1915144/led", System.Text.Encoding.UTF8.GetBytes(data), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
				Debug.Log("Led tranfer to OFF");
			}
			else if (led.switchState == false)
			{
				string data = "{\"device\": \"LED\",\"status\": \"ON\"}";
				client.Publish("/bkiot/1915144/led", System.Text.Encoding.UTF8.GetBytes(data), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
				Debug.Log("Led tranfer to ON");
			}
			led.SetStatus(!led.switchState);
		}

		public void switchButtonPump()
		{
			if (pump.switchState == true)
			{
				string data = "{\"device\": \"PUMP\",\"status\": \"OFF\"}";
				client.Publish("/bkiot/1915144/pump", System.Text.Encoding.UTF8.GetBytes(data), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
				Debug.Log("Pump tranfer to OFF");
			}
			else if (pump.switchState == false)
			{
				string data = "{\"device\": \"PUMP\",\"status\": \"ON\"}";
				client.Publish("/bkiot/1915144/pump", System.Text.Encoding.UTF8.GetBytes(data), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
				Debug.Log("Pump tranfer to ON");
			}
			pump.SetStatus(!pump.switchState);
		}
		private void OnDestroy()
		{
			Disconnect();
		}

		private void OnValidate()
		{
			//if (autoTest)
			//{
			//    autoConnect = true;
			//}
		}

		public void UpdateConfig()
		{

		}

		public void UpdateControl()
		{

		}
	}
}