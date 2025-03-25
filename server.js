const express = require("express");
const { exec } = require("child_process");
const path = require("path");
const uuid = require("uuid");
const app = express();
const cors = require("cors");
const fs = require("fs");

app.use(cors());
app.use(express.json());
app.use("/Back/Videos", express.static(path.join(__dirname, "Videos")));  // Statik dosyalar için 'Videos' klasörünü sunuyoruz

// Video indirme işlemi
app.post("/download", (req, res) => {
  const videoUrl = req.body.url;

  // Benzersiz dosya adı oluşturuyoruz
  const videoName = `${uuid.v4()}.mp4`;  
  const downloadPath = path.join(__dirname, "Videos", videoName);

  // Python betiğini çalıştırarak video indiriyoruz
  exec(`python youtubeDownloader.py "${videoUrl}" "${downloadPath}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      console.error(`stderr: ${stderr}`);
      res.status(500).send("Video indirme hatası!");
      return;
    }

    console.log(stdout);  // Çıktıyı konsola yazdırıyoruz
    // Video başarılı bir şekilde indirildiyse, video URL'sini döndürüyoruz
    res.json({ videoUrl: `/Back/Videos/${videoName}` });

    // 10 dakika sonra video dosyasını sil
    setTimeout(() => {
      if (fs.existsSync(downloadPath)) {
        fs.unlink(downloadPath, (err) => {
          if (err) {
            console.error(`Dosya silme hatası: ${err}`);
          } else {
            console.log(`Video dosyası başarıyla silindi: ${downloadPath}`);
          }
        });
      }
    }, 10 * 60 * 1000); // 10 dakika = 600,000 ms
  });
});

app.listen(5000, () => {
  console.log("Server 5000 portunda çalışıyor...");
});
