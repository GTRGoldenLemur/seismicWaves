const data = [[, , , , , ], [, , , , , , ], [ , , , , , , , ]]

var tracks_p = [0, 1, 2]
var tracks = []
var tSel = 0
var ps = ["moon", "earth", "mars"]
var body = undefined

var mobile = false

window.onload = () => {
	tracks_p = [0, 1, 2]

	tracks = [document.getElementById("wave_track1"), document.getElementById("wave_track2"), document.getElementById("wave_track3")]
	body = document.getElementsByTagName('body')[0]

	sel_track(tSel)

	check_phone();

}

window.onresize = () => {check_phone();}


function check_phone () {
	var a = Math.max(window.innerWidth, window.innerHeight)/Math.min(window.innerHeight, window.innerWidth)
	var b = window.innerWidth/window.innerHeight
	var w = document.getElementById("mobile_wrap_menu")

	if (b < 1.3) {
		body.classList.add("mobile")
		body.appendChild(w)
		body.style.width = "calc( 100% - "+String(body.offsetWidth - body.clientWidth)
		var adjust = setTimeout(undefined, 100)
		body.onscroll = () => {
			if (w.getBoundingClientRect().top < Math.max(300, window.innerHeight*0.4)) {
				shadow(true)
			} else {
				shadow(false)
			}
			clearTimeout(adjust)
			adjust = setTimeout(()=>{
				if (w.getBoundingClientRect().top < Math.max(400, window.innerHeight*0.6)) {
					w.scrollIntoView({behavior: "smooth", block: "start"})
				} else {
					document.getElementById("scrollTop").scrollIntoView({behavior: "smooth", block: "end"})
				}
			}, 300)
		}

		mobile = true

	} else {
		body.classList.remove("mobile")
		document.getElementById('waves_compare').appendChild(w)
		document.getElementById("waves_compare").onclick = null
		body.onscroll = null;
		shadow(false)

		mobile = false
	}
}

function shadow(b) {
	var s = document.getElementById("shadow")
	if (b) {
		s.style.top = "0px"
		s.style.opacity = 0.4
		setTimeout(()=>{s.style.top = "0px"}, 400)

	} else {
		s.style.opacity = 0
		setTimeout(()=>{s.style.top = "-99vh"}, 400)
	}
	s.onclick = ()=>{
		document.getElementById("scrollTop").scrollIntoView({behavior: "smooth", block: "end"})
	}
}

function sel_track(n, butt) {
	tSel = n

	if (butt == false && mobile == true) {
		return
	}

	getPlanet(tracks_p[n])

	for (var i = 0; i < tracks.length; i++) {
		tracks[i].classList.remove("selected_track")
	}

	tracks[n].classList.add("selected_track")

	document.getElementById("menu_heading").innerText = "Change Wave Track "+String(n+1)

	
}

function getPlanet(n) {
	var bR = document.getElementById("sel_right")
	var bL = document.getElementById("sel_left")

	document.getElementById(["sel_moon", "sel_earth", "sel_mars"][n]).scrollIntoView({"behavior": "smooth", "inline": "center"})

	bL.style.left = String(n*100)+"%"
	bR.style.right = String(-n*100)+"%"

	if (n != 2) {
		bR.onclick = () => {
			getPlanet(n+1)
		}
		bR.disabled = false
	} else {
		bR.disabled = true
	}

	if (n != 0) {
		bL.onclick = () => {
			getPlanet(n-1)
		}
		bL.disabled = false
	} else {
		bL.disabled = true
	}

	tracks_p[tSel] = n

	for (var i = 0; i < ps.length; i++) {
		tracks[tSel].classList.remove("wave_"+ps[i])
	}

	tracks[tSel].classList.add("wave_"+ps[n])

	document.getElementById("seismic_heading").innerText = "Pick "+["A Moon", "An Earth", "A Mars"][n]+" Seismic Wave"


	var html = ""

	for (var d = 0; d < data[n].length; d++) {
		html += "<div class=''></div>"
	}

	document.getElementById("seismic_sel").innerHTML = html

}