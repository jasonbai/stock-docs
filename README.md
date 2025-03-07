# 股票数据复盘报告网站

这是一个使用 MkDocs 构建的静态网站，用于展示股票数据复盘报告。

## 功能特点

- 自动分类：根据文件名自动将报告分类为日报、周报和月报
- 自动更新：当新报告添加到 `reports` 目录时，网站会自动更新
- 响应式设计：适配各种设备屏幕大小
- 搜索功能：支持全文搜索报告内容

## 目录结构

```
.
├── docs/                # 文档源文件
│   ├── assets/          # 静态资源
│   │   ├── css/         # 自定义 CSS
│   │   └── js/          # 自定义 JavaScript
│   ├── reports/         # 报告文件
│   │   ├── daily/       # 日报
│   │   ├── weekly/      # 周报
│   │   ├── monthly/     # 月报
│   │   └── other/       # 其他报告
│   └── index.md         # 首页
├── scripts/             # 脚本文件
│   └── generate_nav.py  # 自动生成导航脚本
├── .github/             # GitHub 配置
│   └── workflows/       # GitHub Actions 工作流
│       └── deploy.yml   # 部署工作流
└── mkdocs.yml           # MkDocs 配置文件
```

## 如何使用

### 本地开发

1. 安装依赖：

```bash
pip install mkdocs mkdocs-material mkdocs-git-revision-date-localized-plugin mkdocs-minify-plugin pymdown-extensions
```

2. 本地预览：

```bash
cd docs_site
mkdocs serve
```

3. 构建网站：

```bash
cd docs_site
mkdocs build
```

### 添加新报告

1. 在项目根目录的 `reports` 文件夹中添加新的 Markdown 文件
2. 文件命名规则：
   - 日报：包含 `daily` 或日期格式 `YYYYMMDD` 的文件名
   - 周报：包含 `weekly` 的文件名
   - 月报：包含 `monthly` 的文件名
3. 推送到 GitHub 仓库，GitHub Actions 会自动构建并发布网站

## 自动化流程

当新的报告添加到 `reports` 目录时：

1. GitHub Actions 检测到变化
2. 自动运行 `generate_nav.py` 脚本，将报告分类并更新导航
3. 构建 MkDocs 网站
4. 部署到 GitHub Pages

## 自定义

- 修改 `mkdocs.yml` 文件可以自定义网站设置
- 修改 `docs/assets/css/extra.css` 可以自定义样式
- 修改 `docs/assets/js/extra.js` 可以添加自定义功能 # 触发工作流
