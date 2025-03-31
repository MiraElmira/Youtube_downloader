const express = require("express");
const { exec } = require("child_process");
const path = require("path");
const uuid = require("uuid");
const app = express();
const cors = require("cors");
const fs = require("fs");
const dotenv = require('dotenv')
.config();

app.use(cors());
app.use(express.json());
app.use("/Back/Videos", express.static(path.join(__dirname, "Videos")));  // Serving static files from 'Videos' directory

// Video download process
app.post("/download", (req, res) => {
  const videoUrl = req.body.url;

  // Generating a unique file name
  const videoName = `${uuid.v4()}.mp4`;  
  const downloadPath = path.join(__dirname, "Videos", videoName);

  // Running Python script to download video
  exec(`python youtubeDownloader.py "${videoUrl}" "${downloadPath}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Execution error: ${error}`);
      console.error(`stderr: ${stderr}`);
      res.status(500).send("Video download error!");
      return;
    }

    console.log(stdout);  // Logging output to console
    // If the video is successfully downloaded, return the video URL
    res.json({ videoUrl: `/Back/Videos/${videoName}` });

    // Delete video file after 5 minutes
    setTimeout(() => {
      if (fs.existsSync(downloadPath)) {
        fs.unlink(downloadPath, (err) => {
          if (err) {
            console.error(`File deletion error: ${err}`);
          } else {
            console.log(`Video file successfully deleted: ${downloadPath}`);
          }
        });
      }
    }, 5 * 60 * 1000); // 5 minutes = 300,000 ms
  });
});

app.listen(process.env.PORT, () => {
  console.log(`Server is running on port ${process.env.PORT}...`);
});
