<h2>对 bilibili 竞技游戏区块，上传稿件信息的抓取</h2></br>
<p>使用 Scrapy 框架进行爬取，代理选择的讯代理。其中添加 SeleniumMiddleWare,实现对竞技游戏首页的爬取。</br>
再使用 VideoMiddleWare 对各个视频信息进行内容的爬取。</br><p>
<p>添加了 TextPipeLine 对 Item 进行处理。</br>
之后由 MongoPipeLine 将 Item 存储</p></br>
<p>最后使用 pygal 生成数据图</p></br>
<p>其结果如下图所示</p></br。

<img src="data/result.png">
<img src="data/result_visual.svg">
