# 📚 Netlify部署指南

## 🚀 快速部署步骤

### 方法一：通过Netlify网站部署（推荐）

1. **打包项目**
   ```bash
   cd nextjs-app
   npm run build
   ```
   构建完成后会生成 `out` 文件夹

2. **访问Netlify**
   - 打开 https://app.netlify.com
   - 注册/登录账号（支持GitHub登录）

3. **拖拽部署**
   - 在Netlify首页找到 "Sites" 部分
   - 直接将 `out` 文件夹拖拽到页面上的虚线框内
   - 等待上传完成（约30秒）

4. **获取访问地址**
   - 部署成功后会自动生成一个链接
   - 格式：`https://随机名称.netlify.app`
   - 点击即可访问你的应用！

### 方法二：通过CLI部署

1. **安装Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```

2. **登录Netlify**
   ```bash
   netlify login
   ```

3. **部署到Netlify**
   ```bash
   cd nextjs-app
   netlify deploy --dir=out --prod
   ```

4. **自定义站点名称**
   ```bash
   netlify sites:create --name 你的站点名称
   netlify deploy --dir=out --prod
   ```

## 🎯 自定义域名（可选）

1. 在Netlify控制台选择你的站点
2. 点击 "Domain settings"
3. 添加自定义域名
4. 按照提示配置DNS

## 📝 重要说明

- **免费额度**：每月100GB流量，足够数千用户访问
- **国内访问**：Netlify有全球CDN，国内访问速度较好
- **自动HTTPS**：自动配置SSL证书
- **持续部署**：可以连接GitHub仓库自动部署

## 🔄 更新部署

当你修改代码后，重新部署：

```bash
# 重新构建
npm run build

# 重新部署
netlify deploy --dir=out --prod
```

## 🌏 访问地址示例

部署成功后，你会获得类似这样的地址：
- 临时地址：`https://gracious-newton-123456.netlify.app`
- 自定义地址：`https://ai-media-agent.netlify.app`（需要在Netlify设置）

## ⚠️ 注意事项

1. 确保 `npm run build` 成功执行
2. `out` 文件夹包含所有静态文件
3. 首次部署可能需要1-2分钟
4. 国内用户访问速度取决于网络环境

## 🎉 部署成功标志

- 能访问首页
- 点击"开始航海"按钮正常跳转
- AI聊天助手图标显示在右下角
- 21天学习计划正常显示

---

**需要帮助？** 
- Netlify文档：https://docs.netlify.com
- 常见问题：检查 `out` 文件夹是否存在