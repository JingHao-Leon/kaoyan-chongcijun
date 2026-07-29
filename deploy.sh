#!/bin/bash
# 考研冲刺君 - 一键部署脚本
# 用法：bash deploy.sh
# 作用：把本地 website/ 同步到阿里云服务器，并把改动提交到 GitHub 备份

set -e
cd "$(dirname "$0")/website"

echo "==> 1/2 同步到阿里云 zehaowang.xin ..."
rsync -az --delete --exclude=.git -e "ssh -i ~/.ssh/id_ed25519_aliyun" \
  ./ root@118.31.251.184:/var/www/kaoyan/
echo "    服务器已更新：https://zehaowang.xin"

echo "==> 2/2 提交到 GitHub ..."
git add -A
if git diff --cached --quiet; then
  echo "    没有新改动，跳过提交"
else
  git commit -m "更新：$(date '+%Y-%m-%d %H:%M')"
  git push "https://x-access-token:$(gh auth token)@gh-proxy.com/https://github.com/JingHao-Leon/kaoyan-chongcijun.git" main
  echo "    GitHub 已备份"
fi

echo "==> 完成 ✅"
