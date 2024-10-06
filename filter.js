
var extra_light_blue= "#d3d3d6"
var light_blue= "#9a9ab3"
var dark_blue= "#141424"



function read_file(name, after) {
	var f = new XMLHttpRequest()
	path = name
	f.open("GET", path, true)
	f.send()
	f.onreadystatechange = function()
    {	

    	if (this.readyState == 4 && this.status == 200) {


			allText = f.responseText;

			//console.log(f.responseText)

			wave_data = f.responseText.split("\r\n")

			//console.log(wave_data)

			start = wave_data[1].split(",")[0]

			table_d = []

			for (var i = 0; i < wave_data.length; i++) {
				table_d.push(wave_data[i].split(",").slice(1, 3))
			}

			after(table_d.slice(0, (table_d).length-1), start)

    	}

    };
}

function get_quakes(name, after) {
	var f = new XMLHttpRequest()
	path = name
	f.open("GET", path, true)
	f.send()
	f.onreadystatechange = function()
    {	

    	if (this.readyState == 4 && this.status == 200) {
			allText = f.responseText;
			//console.log(f.responseText)

			wave_data = f.responseText.split("\r\n")

			table_d = []

			for (var i = 0; i < wave_data.length; i++) {
				table_d.push(wave_data[i].split(",").slice(1, 3))
			}

			after(table_d.slice(0, (table_d).length))

    	}

    };
}

function fill_track(path, t) {

	console.log("Opening on track "+t)
	document.querySelectorAll("#wave_track"+t+" .loading")[0].classList.remove("hide_load")

	read_file(path+".LightData.csv", (a, b)=>{
		get_quakes(path+".Quakes.csv", (q)=>{
			fill_canvas(a, t, b, q)	
		})
	})
}


function fill_canvas(d, t, time, quakes) {
	var c = document.getElementById("wave_canv_t"+String(t))


	width = c.width - 40
	height = c.height - 40

	padding = 20

	ctx = c.getContext("2d");

	ctx.clearRect(0, 0, width, height)

	var g = new Path2D()

	g.moveTo(padding, height/2)

	var max_y = 8*10**-9
	ctx.lineWidth = 4
	var interval= 10

	if (tracks_p[t-1] == 2) {
		max_y = 3000

		for (var i = 1; i < d.length; i++) {
			max_y = Math.max(d[i][1], max_y)
		}

		ctx.lineWidth = 5
		console.log("Mars detected...")
		interval = 1
		max_y*=2

	}

	for (var i = 1; i < d.length; i++) {

		x = d[i][0]/d[ d.length-1 ][0] *width
		y = height/2 + d[i][1]/(max_y)*height

		if (x && y) {
			g.lineTo(x, y)
		} else {
			//console.log(x, y, d[i][0], d[i][1])			
		}


		i += interval
	}

	document.querySelectorAll("#wave_track"+t+" .loading")[0].classList.add("hide_load")

	console.log("DONE opening "+time+" in track "+t)

	ctx.strokeStyle = light_blue+"dd"
	ctx.stroke(g)

	for (var n = 0; n < quakes.length; n++) {
		q = quakes[n]

		console.log(q)

		x1 = q[0]/d[ d.length-1 ][0] *width
		x2 = q[1]/d[ d.length-1 ][0] *width

		var fillR = new Path2D()
		fillR.moveTo(x1, padding+10)
		fillR.lineTo(x2, padding+10)
		fillR.lineTo(x2, padding+height-10)
		fillR.lineTo(x1, padding+height-10)

		ctx.fillStyle = dark_blue+"99"
		ctx.fill(fillR)


		ctx.lineWidth = 12

		var sLine = new Path2D()
		sLine.moveTo(x1, padding)
		sLine.lineTo(x1, padding+height)
		ctx.strokeStyle = extra_light_blue
		ctx.stroke(sLine)

		var eLine = new Path2D()
		eLine.moveTo(x2, padding)
		eLine.lineTo(x2, padding+height)
		ctx.strokeStyle = extra_light_blue
		ctx.stroke(eLine)		


	}

}


function zoom(t, r) {
	tracks_z[t] *= r

	var z_i = document.querySelectorAll("#wave_track"+String(t+1)+" .zoom_in")[0]
	var z_o = document.querySelectorAll("#wave_track"+String(t+1)+" .zoom_out")[0]

	z_i.disabled = false; z_o.disabled = false

	if (tracks_z[t] == 0.5){
		z_o.disabled = true
	} else if (tracks_z[t] == 8) {
		z_i.disabled = true
	}
	check_phone()

}