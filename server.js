const express = require("express");
const path = require("path");
const fs = require("fs"); // Dosya sistemi modülü
const { exec } = require("child_process");
const app = express();
const cors = require("cors");

app.use(cors());
app.use(express.json());

// Video dizini
const videoDirectory = path.join(__dirname, "Videos");

app.post("/download", (req, res) => {
  const videoUrl = req.body.url;
  const videoPath = path.join(videoDirectory, "downloaded_video.mp4");

  // Python betiğini çalıştırarak video indiriyoruz
  exec(`python youtubeDownloader.py "${videoUrl}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      res.status(500).send("Video indirme hatası!");
      return;
    }

    // Dosya başarıyla indirildiyse, video dosyasını kullanıcıya gönderiyoruz
    res.download(videoPath, "downloaded_video.mp4", (err) => {
      if (err) {
        console.error("Dosya gönderim hatası:", err);
        res.status(500).send("Dosya gönderilemedi!");
      }
    });
  });
});

app.listen(5000, () => {
  console.log("Server 5000 portunda çalışıyor...");
});
