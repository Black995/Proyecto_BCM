/*
interface Duration {
	days: number
	hours: number
	minutes: number
}
*/
export function setRecoveryTime(duration) {
	let day = ''
	let hour = ''
	let minute = ''

	if (duration.days <= 9) day = '0' + duration.days.toString()
	else day = duration.days.toString()

	if (duration.hours <= 9) hour = '0' + duration.hours.toString()
	else hour = duration.hours.toString()

	if (duration.minutes <= 9) minute = '0' + duration.minutes.toString()
	else minute = duration.minutes.toString()

	return day + ' ' + hour + ':' + minute + ':00'
}

export function getRecoveryTime(durationText) {

	const duration = {
		days: 0,
		hours: 0,
		minutes: 0
	}
	let stringArray = []

	//Verificamos si el string tiene espacios (para separar días)
	if(durationText.indexOf(' ') >= 0) {
		stringArray = durationText.split(" ");
		duration.days = parseInt(stringArray[0]);
		duration.hours = parseInt(stringArray[1].slice(0,2))
		duration.minutes = parseInt(stringArray[1].slice(3,5))
	}
	else {
		duration.days = 0;
		duration.hours = parseInt(durationText.slice(0,2))
		duration.minutes = parseInt(durationText.slice(3,5))
	}
	
	return duration;
}

export function getRecoveryTimeText(durationText) {

	const duration = {
		days: 0,
		hours: 0,
		minutes: 0
	}
	let stringArray = []
	let text = '';

	//Verificamos si el string tiene espacios (para separar días)
	if(durationText.indexOf(' ') >= 0) {
		stringArray = durationText.split(" ");
		duration.days = parseInt(stringArray[0]);
		duration.hours = parseInt(stringArray[1].slice(0,2))
		duration.minutes = parseInt(stringArray[1].slice(3,5))
		text = duration.days.toString() + ' días, ' + duration.hours.toString() + ' horas, ' + duration.minutes.toString() + ' minutos'
	}
	else {
		duration.days = 0;
		duration.hours = parseInt(durationText.slice(0,2))
		duration.minutes = parseInt(durationText.slice(3,5))
		text = duration.hours.toString() + ' horas, ' + duration.minutes.toString() + ' minutos'
	}
	
	return text;
}
