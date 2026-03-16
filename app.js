function loadErg(){

const file = document.getElementById("ergFile").files[0]

const reader = new FileReader()

reader.onload = function(e){

const text = e.target.result
const rows = text.split("\n").slice(1)

let watts = []

rows.forEach(row=>{

const cols = row.split(",")

if(cols[3]){
watts.push(Number(cols[3]))
}

})

drawChart(watts)

}

reader.readAsText(file)

}

function drawChart(data){

const ctx = document.getElementById("ergChart")

new Chart(ctx,{
type:"line",
data:{
labels:data.map((_,i)=>i),
datasets:[{
label:"Watts",
data:data
}]
}
})

}

function loadVideo(){

const file = document.getElementById("videoFile").files[0]

const url = URL.createObjectURL(file)

document.getElementById("videoPlayer").src = url

}
