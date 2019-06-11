<html>
<head>
</head>
<body>
    <h1>檔案上傳進度...</h1>
<?php
# 檢查檔案是否上傳成功
if ($_FILES['my_file']['error'] === UPLOAD_ERR_OK){
  echo '檔案名稱: ' . $_FILES['my_file']['name'] . '<br/>';
  echo '檔案類型: ' . $_FILES['my_file']['type'] . '<br/>';
  echo '檔案大小: ' . ($_FILES['my_file']['size'] / 1024) . ' KB<br/>';
  echo '暫存名稱: ' . $_FILES['my_file']['tmp_name'] . '<br/>';

  # 檢查檔案是否已經存在
  if (file_exists('upload/' . $_FILES['my_file']['name'])){
    echo '檔案已存在。<br/>';
  } else {
    $file = $_FILES['my_file']['tmp_name'];
    $dest = 'upload/' . $_FILES['my_file']['name'];

    # 將檔案移至指定位置
    move_uploaded_file($file, $dest);
    
    system("bash video2mpd.sh upload");
    $name = explode('.', $_FILES['my_file']['name']);
    $oldPath = 'upload/' . $name[0];
    $newPath = 'video/' . $name[0];
    rename($oldPath, $newPath);

    //重定向瀏覽器 
    header("Location: http://localhost:8080"); 
    //確保重定向後，後續代碼不會被執行 
    exit;
  }
} else {
  echo '錯誤代碼：' . $_FILES['my_file']['error'] . '<br/>';
}

?>
<a href="http://localhost:8080">若無跳轉頁面，按此重回原頁面</a>
</body>