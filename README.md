SW_NewsUpdate用于抓取各网站更新的关于固废的文章；
AW_NewsUpdate用于抓取各网站更新的关于大气和水体污染的文章；

这两个脚本的工作原理都是一样的，首先抓取网站上最新的12篇文章的标题和链接，然后逐个将这些文章的标题与历史文章列表进行比对，如果有哪篇文章的标题不在历史列表里，就认为它是新文章，把它写入html网页文件里。写入完毕后，就把这篇文章的标题和链接加到历史文章标题列表里。历史列表存储在AW_NewsHistory.csv和SW_NewsHistory.csv两个文件里。
