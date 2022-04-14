using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using DG.Tweening;
using System;

public class SwitchButton : MonoBehaviour
{
	public bool switchState = false;
	public GameObject switchBtn;

	public void OnSwitchButtonClicked()
	{
		switchBtn.transform.DOLocalMoveX(-switchBtn.transform.localPosition.x, 0.2f);
		// switchState = Math.Sign(-switchBtn.transform.localPosition.x);
		// switchState = !switchState;
		// Debug.Log("Button Current State: " + switchState);
	}

	public void SetStatus(bool state)
	{
		// Debug.Log("Current State: " + state);
		// Debug.Log("Old State: " + switchState);
		if (switchState != state)
		{
			OnSwitchButtonClicked();
			switchState = state;
		}
	}
}