# 🚀 从GitHub部署到Netlify - 超简单指南

## ✅ 代码已推送到GitHub

你的项目已经成功推送到：
**https://github.com/guasi18587278913/Hanghai-Agent.git**

## 📋 Netlify部署步骤（3分钟搞定）

### 1️⃣ 登录Netlify
访问 https://app.netlify.com 并登录（推荐用GitHub账号登录）

### 2️⃣ 导入GitHub项目

1. 点击 **"Add new site"** → **"Import an existing project"**
2. 选择 **"Deploy with GitHub"**
3. 授权Netlify访问你的GitHub
4. 搜索并选择 **"Hanghai-Agent"** 仓库

### 3️⃣ 配置构建设置

在部署配置页面，填写以下信息：

```
Branch to deploy: master
Base directory: ai-media-agent/nextjs-app
Build command: npm run build
Publish directory: ai-media-agent/nextjs-app/out
```

**重要提示**：
- Base directory 必须设置为 `ai-media-agent/nextjs-app`
- Publish directory 必须设置为 `ai-media-agent/nextjs-app/out`

### 4️⃣ 点击Deploy

点击 **"Deploy site"** 按钮，等待2-3分钟

### 5️⃣ 获取访问链接

部署成功后，你会获得一个链接：
- 临时链接：`https://xxx-xxx-xxx.netlify.app`
- 可以在Site settings中修改为更友好的名称

## 🎯 一键部署按钮（更快速）

你也可以使用这个按钮一键部署：

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/guasi18587278913/Hanghai-Agent)

## ⚙️ 环境变量（可选）

如果需要添加环境变量：
1. 在Netlify控制台进入你的站点
2. 点击 **Site settings** → **Environment variables**
3. 添加需要的变量

## 🔄 自动部署

设置成功后，每次推送到GitHub都会自动部署：
```bash
git add .
git commit -m "更新内容"
git push origin master
```

## 📱 自定义域名（可选）

1. 在Netlify控制台选择你的站点
2. 点击 **Domain settings**
3. 点击 **Add custom domain**
4. 输入你的域名并按提示配置DNS

## ✨ 部署成功后

访问你的站点，你应该能看到：
- 🎯 航海主题的首页
- 📝 智能评测系统
- 📅 21天学习计划
- 💬 AI聊天助手（右下角）
- 📚 查看航海手册链接

## 🆘 常见问题

**Q: 构建失败？**
A: 检查Base directory是否设置正确：`ai-media-agent/nextjs-app`

**Q: 404错误？**
A: 检查Publish directory是否设置正确：`ai-media-agent/nextjs-app/out`

**Q: 页面样式丢失？**
A: 清除浏览器缓存，或等待CDN刷新（约5分钟）

## 🎉 恭喜！

你的AI自媒体学习平台已经上线了！
分享链接给朋友们体验吧！

---

**需要帮助？**
- Netlify文档：https://docs.netlify.com
- 项目仓库：https://github.com/guasi18587278913/Hanghai-Agent