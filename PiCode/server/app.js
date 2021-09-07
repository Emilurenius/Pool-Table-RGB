// All external modules are loaded in:
const express = require("express")
const app = express()
const bodyParser = require("body-parser")
const path = require("path")
const fs = require("fs")
const cors = require("cors")
const cookieParser = require("cookie-parser")
const bcrypt = require("bcrypt")

let ballsDown = []

function loadJSON(filename) {
    const rawdata = fs.readFileSync(path.join(__dirname, filename))
    const data = JSON.parse(rawdata)
    return data
}

function saveJSON(json, filename) {
    const stringified = JSON.stringify(json, null, 4)
    fs.writeFile(path.join(__dirname, filename), stringified, (err) => {
        if (err) throw err
        console.log("Data written to file")
    })
}

// Reading input from terminal start
const port = parseInt(process.argv[2])
console.log(`${port} registered as server port`)
// Reading input from terminal end

//Here we are configuring express to use body-parser as middle-ware.
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
app.use(cookieParser()) // Middleware for handling cookies
app.use(cors()) // Making sure the browser can request more data after it is loaded on the client computer.

app.use(cors()) // Making sure the browser can request more data after it is loaded on the client computer.

app.use("/static", express.static("public"))

app.get("/", (req,res) => {
    res.sendFile(path.join(__dirname, "/html/controlPanel.html"))
})

app.get("/ballDown", (req, res) => {
    const hole = req.query.hole

    if (hole >= 0 && hole < 6) {
        console.log(hole)
        ballsDown.push(hole)
    }
    res.send(`Hole = ${hole}`)
})

app.get("/getBallsDown", (req, res) => {
    res.send(ballsDown)
    ballsDown = []
})


app.listen(port, () => console.log(`Listening on ${port}`))