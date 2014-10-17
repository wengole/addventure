private var motor : CharacterMotor;

// Use this for initialization
function Awake () {
	motor = GetComponent(CharacterMotor);
}

function GoGoGadget () {
	//var url = "http://www.random.org/integers/?num=1&min=1&max=10&col=1&base=10&format=plain&rnd=new";
	var url = "http://localhost:8080/";
	var www : WWW = new WWW (url);
    while(!www.isDone){
		Debug.Log(www.progress);
	}
	return www;
}

// Update is called once per frame
function Update () {
	// Get the input vector from keyboard or analog stick
//	var directionVector = new Vector3(Input.GetAxis("Horizontal"), 0, Input.GetAxis("Vertical"));
	
	//Debug.Log("Before");
	/*
	www = GoGoGadget();
	//Debug.Log("After");
	
	if (www.error == null) {
		// request completed!
		Debug.Log("WWW Text: "+ www.text);
		value = parseFloat(www.text);
		value = -0.025 * value;
		var directionVector = new Vector3(value, 0, value);
	} else {
		Debug.Log("WWW Error: "+ www.error);
	//	directionVector = new Vector3(0, 0, 0);	
		return;
	}
	*/
	var directionVector = new Vector3(0.025, 0, 0.025);
	Debug.Log("Move: "+ directionVector);

	if (directionVector != Vector3.zero) {
		// Get the length of the directon vector and then normalize it
		// Dividing by the length is cheaper than normalizing when we already have the length anyway
		var directionLength = directionVector.magnitude;
		directionVector = directionVector / directionLength;
		
		// Make sure the length is no bigger than 1
		directionLength = Mathf.Min(1, directionLength);
		
		// Make the input vector more sensitive towards the extremes and less sensitive in the middle
		// This makes it easier to control slow speeds when using analog sticks
//		directionLength = directionLength * directionLength;
		
		// Multiply the normalized direction vector by the modified length
		directionVector = directionVector * directionLength;
	}
	
	// Apply the direction to the CharacterMotor
	motor.inputMoveDirection = transform.rotation * directionVector;
//	motor.inputJump = Input.GetButton("Jump");
}

// Require a character controller to be attached to the same game object
@script RequireComponent (CharacterMotor)