# Time Management

## 前言

現代人因為休閒娛樂增多，對於自身的時間掌控度比較沒有概念。此次設計出來的APP就是希望能讓使用者慢慢的意識到時間規劃的重要性，檢視一日所做的事，以及花費的時間量。

## 構想

此APP有三個主要的功能，分別如下:

    -add: 增加行程
    -show: 顯示一日的行程規劃
        -schedule: 列出行程表
        -statistic: 顯示一日所花的時間比例
    -change: 改變輸入資訊
        -act: 行程資訊
        -time: 單一行程時間
        -tag: 行程標籤

## 環境

    作業系統: Ubuntu 18.04.4 LTS
    python 版本: Python 3.6.9

## 使用說明


最初始的狀態在main menu
當使用者輸入add，linebot就會要求使用者輸入起始與結束時間。
![](https://i.imgur.com/sj95dmI.jpg)

接著使用者要輸入想加入的行程，並且用標籤記錄行程性質，最後會顯示輸入成功的訊息。
![](https://i.imgur.com/oTK6jdy.jpg)
在輸入tag時，linebot會顯示目前已經存在的標籤們。
![](https://i.imgur.com/bxgQv0S.jpg)
回到主目錄。
![](https://i.imgur.com/RPQihvz.jpg)
輸入show，進到下一個選單。
![](https://i.imgur.com/8bP03bg.jpg)
輸入schedule，顯示行程時間表。
![](https://i.imgur.com/lyDEtkm.jpg)
輸入statistic，顯示每個tag之下的的行程總共花費時間的紀錄。
![](https://i.imgur.com/7TGNxPU.jpg)
回到主目錄，選擇change，接著進入下一個選單。
![](https://i.imgur.com/9VF24DI.jpg)
輸入act，代表想要更換行程名稱，接著linebot會顯示目前所有的行程。
![](https://i.imgur.com/wqHHhMF.jpg)
接著使用者輸入新的行程名稱，linebot會顯示已更新成功的訊息。
![](https://i.imgur.com/Dub96lg.jpg)
輸入continue回到次目錄，輸入time後，linebot一樣會顯示出所有的行程。
![](https://i.imgur.com/fjGOuGj.jpg)
選擇要被更新時間的行程。
![](https://i.imgur.com/9nWjRzh.jpg)
輸入新的起始時間與結束時間後，linebot一樣會顯示更新成功的訊息。
![](https://i.imgur.com/SfkQcx5.jpg)
如下圖，進入schedule可以看到sleep成功被更新。
![](https://i.imgur.com/l67W36K.jpg)
進入statistic也可以發現sleep相對應的tag，daily增加時間長度。
![](https://i.imgur.com/xH5boYj.jpg)
回到次目錄，選擇tag，linebot顯示所有的行程。
![](https://i.imgur.com/De5Lny8.jpg)
輸入欲更換標籤的行程，接著輸入新的標籤名稱。
![](https://i.imgur.com/oR85gAj.jpg)
可以看到舊標籤的時間替換到新的標籤。
![](https://i.imgur.com/T2qZAdq.jpg)


## FSM

![](https://i.imgur.com/8vvytNV.png)


