const data = [[["https://gtrgoldenlemur.github.io/seismicWaves/data/MoonWave2", "1971-06-11T00:00:00.743943"] , ["https://gtrgoldenlemur.github.io/seismicWaves/data/MoonWave1", "1970-10-26T00:00:00.287943"], ["https://gtrgoldenlemur.github.io/seismicWaves/data/MoonWave3", "1972-11-19T00:00:00.826943"], ["https://gtrgoldenlemur.github.io/seismicWaves/data/MoonWave4", "1972-01-26T00:00:00.488943"], ["https://gtrgoldenlemur.github.io/seismicWaves/data/MoonWave5", "1973-10-03T03:59:12.764190"], ["https://gtrgoldenlemur.github.io/seismicWaves/data/MoonWave6", "1970-09-09T00:00:00.275943"], ["https://gtrgoldenlemur.github.io/seismicWaves/data/MoonWave7", "1971-06-27T00:00:00.381943"], ["https://gtrgoldenlemur.github.io/seismicWaves/data/MoonWave8", "1974-03-14T00:00:00.531943"], ["https://gtrgoldenlemur.github.io/seismicWaves/data/MoonWave9", "1975-05-20T00:00:00.704943"]], [], [["https://gtrgoldenlemur.github.io/seismicWaves/data/MarsWave1", "2019-05-23T02:00:00.082000"], ["https://gtrgoldenlemur.github.io/seismicWaves/data/MarsWave2", "2019-09-21T03:00:00.087000"], ["https://gtrgoldenlemur.github.io/seismicWaves/data/MarsWave3", "2021-12-24T22:00:00.091000"], ["https://gtrgoldenlemur.github.io/seismicWaves/data/MarsWave4", "2022-05-04T23:00:00.098000"], ["https://gtrgoldenlemur.github.io/seismicWaves/data/MarsWave5", "2022-01-02T04:00:00.075000"]]];

var tracks_p = [0, 1, 2]
var tracks_z = [1, 1, 1]
var tracks = []
var tSel = 0
var ps = ["moon", "earth", "mars"]
var body = undefined

var mobile = false

window.onload = () => {
	tracks_p = [0, 1, 2]

	tracks = [document.getElementById("wave_track1"), document.getElementById("wave_track2"), document.getElementById("wave_track3")]
	body = document.getElementsByTagName('body')[0]

	sel_track(tSel);
	document.getElementById("sel_moon").scrollIntoView({"inline": "center", behavior: "smooth"})

	check_phone();

	//fill_track("https://gtrgoldenlemur.github.io/seismicWaves/data/MoonWave2", 1)

}

window.onresize = () => {check_phone();}


function check_phone () {
	var a = Math.max(window.innerWidth, window.innerHeight)/Math.min(window.innerHeight, window.innerWidth)
	var b = window.innerWidth/window.innerHeight
	var w = document.getElementById("mobile_wrap_menu")

	if (b < 1.3) {
		body.classList.add("mobile")
		body.appendChild(w)
		//body.style.width = "calc( 100% - "+String(body.offsetWidth - body.clientWidth)
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
			}, 100)
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


	for (var n = 1; n < 4; n++) {

		var canv = document.getElementById("wave_canv_t"+n)
		var cont = document.getElementById("wave_cont_t"+n)

		var z = tracks_z[n-1]

		canv.style.display = "none"
		cont.style.maxHeight = ""
		cont.style.maxWidth = ""


		setTimeout( ((cont, canv, z)=>{

			cont.style.maxWidth = cont.getBoundingClientRect().width+"px"
			cont.style.maxHeight = cont.getBoundingClientRect().height+"px"

			canv.style.height = (cont.getBoundingClientRect().height-20)+"px"
			canv.style.width = ((cont.getBoundingClientRect().width*z)-20)+"px"


		}).bind(null, cont, canv, z), 20)

		setTimeout(((cont, canv, z)=>{
			canv.style.display = "block"
		}).bind(null, cont, canv, z), 40)
		
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
	console.log(n, document.getElementById(["sel_moon", "sel_earth", "sel_mars"][n]))

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


	if (tracks_p[tSel] != n) {
		clear_track(tSel+1)
	}

	tracks_p[tSel] = n

	for (var i = 0; i < ps.length; i++) {
		tracks[tSel].classList.remove("wave_"+ps[i])
	}

	tracks[tSel].classList.add("wave_"+ps[n])

	document.getElementById("seismic_heading").innerText = "Pick "+["A Moon", "An Earth", "A Mars"][n]+" Seismic Wave"


	var html = ""

	for (var d = 0; d < data[n].length; d++) {
		html += "<div class='' onclick='fill_track("+'"'+data[n][d][0]+'"'+", "+String(tSel+1)+")'>"+data[n][d][1]+"</div>"
	}

	html = html || "<p style='color: var(--extra-light-blue);'>No data available for this planet</p>"

	document.getElementById("seismic_sel").innerHTML = html

}
