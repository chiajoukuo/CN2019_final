# CN2019_final
Computer Network final : video streaming

## Video Player
### How to start
```python3
# Install ffmpeg & mp4box
brew install ffmpeg gpac

# Clone our repo
git clone https://github.com/chiajoukuo/CN2019_final.git
cd video-player

# Create video/ & upload/
mkdir video upload

# Use php to create a web-server
php -S [IP address] # Ex. localhost:8080, 192.168.43.220::8080...

# Go to Chrome and type your IP address
# You can see index.html display on the web page
```
### Change some IP addresses inside index.html & upload.php
**index.html**
```html
<!-- Line 35 -->
<h1>Video Player <a href="http://YOUR_VIDEO_STREAMING_IP_ADDRESS"><img src="non.png" class="icon"/></a></h1>
```
**upload.php**
```php
# Line 46
header("Location: http://YOUR_IP_ADDRESS"); 
# Line 56
<a href="http://YOUR_IP_ADDRESS">若無跳轉頁面，按此重回原頁面</a>
```
### Default Videos
* Avengers 4 Trailer & Michael Wazowski are called video2.mp4 & MU_1.mp4 in our server
* Feel free to delete the default select options in our index.html

### Now you can
* **Upload your own video**
  - You might need to wait a while so that server can have time to convert the video
* **Type the Video Name in Input area, and press Enter**
* **Use the Downdrop Items to Select the Video you want to watch**
* **Switch the playback rate using Button upon the player**

## Refernces
* [socket OpenCV](http://blog.maxkit.com.tw/2017/07/socket-opencv-client.html)
