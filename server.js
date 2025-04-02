const express = require("express");
const { exec } = require("child_process");
const path = require("path");
const uuid = require("uuid");
const app = express();
const cors = require("cors");
const fs = require("fs");
const dotenv = require('dotenv').config();

app.use(cors());
app.use(express.json());
app.use("/Back/Videos", express.static(path.join(__dirname, "Videos")));  // Serving static files from 'Videos' directory

// Video download process
app.post("/download", (req, res) => {
  const videoUrl = req.body.url;
  const formatType = req.body.format || "mp4"; // Varsayılan format mp4
  const fileExtension = formatType === "mp3" ? "mp3" : "mp4";

  // Benzersiz dosya adı oluşturuyoruz (uzantı eklemiyoruz)
  const videoNameBase = uuid.v4();
  const downloadPath = path.join(__dirname, "Videos", videoNameBase);
  // Son dosya adını oluşturuyoruz: base + uzantı
  const finalFileName = `${videoNameBase}.${fileExtension}`;

  // Python betiğini çalıştırıyoruz
  exec(`python youtubeDownloader.py "${videoUrl}" "${downloadPath}" "${formatType}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Execution error: ${error}`);
      console.error(`stderr: ${stderr}`);
      res.status(500).send("Video download error!");
      return;
    }

    console.log(stdout);  // Logging output to console
    // Eğer video başarıyla indirildiyse, video URL'sini gönderiyoruz
    res.json({ videoUrl: `/Back/Videos/${finalFileName}` });

    // 5 dakika sonra dosyayı sil
    setTimeout(() => {
      const fullPath = path.join(__dirname, "Videos", finalFileName);
      if (fs.existsSync(fullPath)) {
        fs.unlink(fullPath, (err) => {
          if (err) {
            console.error(`File deletion error: ${err}`);
          } else {
            console.log(`Video file successfully deleted: ${fullPath}`);
          }
        });
      }
    }, 5 * 60 * 1000);
  });
});

app.listen(process.env.PORT, () => {
  console.log(`Server is running on port ${process.env.PORT}...`);
});
