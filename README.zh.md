# 设计

设计该工具的初衷是能够减少在工作中文档检索时间，能够丝滑的找到想要的内容。文档检索，现就有很多轮子，比如能够检索整个互联网的谷歌、百度等搜索引擎，再比如知乎、stackoverflow等都提供检索，在工作中这些文档检索工具确实也能够解决问题。但是，在解决问题的过程中，有一些感觉不够丝滑的地方，比如：

* 某一个问题，根据一篇文档解决过，因为该文档足够完美，无需自己再次总结，再次遇到该问题时完全可以通过某工具直接定位到该文档。这种情况，最简单的方法是总结一下问题和该文档并附上链接，放到某工具中，比如语雀，可以通过检索语雀找到该文档。
* 因为某种原因，自己的文档被迫放在不同的地方，比如公司自己的文档管理工具和外网的工具中，检索文档需要在两个地方各检索一次。这种情况，还是需要自己把分布在不同的地方的文档数据放到一个检索引擎里面去实现。
* 某轮子提供的检索能力不行，需要自定义功能。

解决上述问题的大概想法：写一个命令行工具，解析一个配置文件，拉取文档数据，放到本地启动的一个 Elasticsearch 服务中，通过调用 Elasticsearch 服务的接口，完成服务的检索。

在解决上述问题的同时，也存在以下优点：
* 配置文件可以灵活定义拉取文档的方式，比如将整个 github repo 或者 语雀repo 拉下来，根据文档的格式实现不同的抽取规则
* Elasticsearch 也可以替换成更加好的更加智能的检索引擎

(就是感觉性价比有点低...)

## 1. 总体流程

**拉取/索引文档**

* 解析配置文件
* [Optional] 判断是否需要更新
* 从网络/本地等源中获取文档
* 解析文档
* 上传的Elasticsearch中

**检索文档**

* 解析用户查询
* 转换成 Elasticsearch 接口调用
* 展示查询结果

## 2. 配置文件

```yaml
elasticsearch_url: 
rules: 
    - <some rule>
    - <some rule>
```

> 其中，elasticsearch_url 指向 elasticsearch 的 url，如果该字段不存在，使用默认的地址 `http://127.0.0.1:9200`
> `some rule` 见后文

## manual_http_urls

```yaml
type: manual_http_urls
title: <a sentence tel everything>
tags: [tag1, tag2, tag3]
summary: <give the summary here if you what, may be tldr>
http_urls: [<the http url>]
```

## manual_file_urls

```yaml
type: manual_file_urls
title: <a sentence tel everything>
tags: [tag1, tag2, tag3]
summary: <give the summary here if you what, may be tldr>
http_urls: [<the http url>]
```

## 3. Elasticsearch Schema

```json
{
    "properties": {
        "title": {},
        "tags": {},
        "summary": {},
        "body": {}
    }
}
```

## 4. 更新规则

* 在解析配置文件中，发现如果 Elasticsearch 中不存在对应的文档时才更新
* Elasticsearch 中如果存在多余的文档，也会被删除
* 通过命令可以强制更新

## 5. 客户端命令设计

**更新文档**

```bash
pq update
pg update --force
```

**查询**

```bash
pg query 'how to do something'
```
