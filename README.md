# page_query

page_query 提供 pq 客户端，与 elasticsearch 一道提供 收集、索引和查询 文档的功能 （主要集中在类似tldr的文档）。

## Tutorial

### 1. 安装 elasticsearch

#### **选择1**

使用 docker 安装 elasticsearch

首先，[安装 docker](https://docs.docker.com/get-docker/)。

然后，通过 docker 来安装 elasticsearch

```
sudo docker pull elasticsearch:7.4.2
sudo docker run -d --name elasticsearch --net page-query -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.4.2
```

#### **选择2**

[直接安装 elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/7.14/install-elasticsearch.html)


### 2. 安装 page_query

```
pip install page_query
```

### 3. 编写 page_query_config.yaml


```yaml
elasticsearch_url: http://localhost:9200
rules:
  - type: manual_http_urls
    title: golang helloworld
    tags: [golang]
    summary: the first program of golang
    http_urls:
      - "https://gobyexample.com/hello-world"
#   - type: manual_http_urls_glob_md
#     glob: 
#     - docs/*.md
```

### 4. 索引 & 查询

```
pq --update
pq
pq --query golang
pq --query 'golang helloworld'
```
