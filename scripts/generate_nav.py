#!/usr/bin/env python3
import os
import yaml
import re
import shutil
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('generate_nav')

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 报告目录 - 修改为直接在 docs/reports 中管理报告
REPORTS_DOCS_DIR = os.path.join(PROJECT_ROOT, 'docs', 'reports')

def extract_title(file_path):
    """从 Markdown 文件中提取标题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 尝试匹配第一个 # 开头的标题
            match = re.search(r'^# (.*?)$', content, re.MULTILINE)
            if match:
                return match.group(1)
            
            # 如果没有找到标题，尝试从文件名中提取日期
            filename = os.path.basename(file_path)
            date_match = re.search(r'(\d{8})', filename)
            if date_match:
                date_str = date_match.group(1)
                try:
                    date_obj = datetime.strptime(date_str, '%Y%m%d')
                    return date_obj.strftime('%Y年%m月%d日') + ' 报告'
                except ValueError:
                    pass
    except Exception as e:
        logger.error(f"读取文件 {file_path} 时出错: {e}")
    
    # 如果无法提取标题，使用文件名
    return os.path.basename(file_path).replace('.md', '')

def get_report_type(filename):
    """根据文件名判断报告类型"""
    if 'daily' in filename.lower() or 'day' in filename.lower():
        return 'daily'
    elif 'weekly' in filename.lower() or 'week' in filename.lower():
        return 'weekly'
    elif 'monthly' in filename.lower() or 'month' in filename.lower():
        return 'monthly'
    
    # 尝试从文件名中提取日期来判断
    date_match = re.search(r'(\d{8})', filename)
    if date_match:
        return 'daily'  # 默认为日报
    
    return 'other'  # 其他类型

def organize_reports():
    """整理报告文件到对应的目录"""
    # 确保各类型报告目录存在
    for report_type in ['daily', 'weekly', 'monthly', 'other']:
        type_dir = os.path.join(REPORTS_DOCS_DIR, report_type)
        if not os.path.exists(type_dir):
            os.makedirs(type_dir)
            logger.info(f"创建目录: {type_dir}")
    
    # 遍历报告目录中的文件
    for item in os.listdir(REPORTS_DOCS_DIR):
        item_path = os.path.join(REPORTS_DOCS_DIR, item)
        
        # 只处理根目录下的 Markdown 文件
        if os.path.isfile(item_path) and item.endswith('.md'):
            report_type = get_report_type(item)
            target_dir = os.path.join(REPORTS_DOCS_DIR, report_type)
            target_path = os.path.join(target_dir, item)
            
            # 如果文件不在对应类型目录中，移动它
            if not os.path.exists(target_path):
                shutil.move(item_path, target_path)
                logger.info(f"移动文件 {item} 到 {report_type} 目录")

def generate_nav():
    """生成 MkDocs 导航配置"""
    nav = [{'首页': 'index.md'}]
    reports_nav = {'报告': []}
    
    # 整理报告文件
    organize_reports()
    
    # 报告类型的中文名称
    type_names = {
        'daily': '日报',
        'weekly': '周报',
        'monthly': '月报',
        'other': '其他报告'
    }
    
    # 处理不同类型的报告
    for report_type in ['daily', 'weekly', 'monthly', 'other']:
        type_dir = os.path.join(REPORTS_DOCS_DIR, report_type)
        if not os.path.exists(type_dir) or not os.listdir(type_dir):
            continue
        
        type_nav = {type_names[report_type]: []}
        
        # 获取该类型下的所有报告
        reports = []
        for file in os.listdir(type_dir):
            if file.endswith('.md'):
                file_path = os.path.join(type_dir, file)
                title = extract_title(file_path)
                reports.append({title: f'reports/{report_type}/{file}'})
        
        # 按文件名排序（假设文件名包含日期）
        reports.sort(key=lambda x: list(x.values())[0], reverse=True)
        
        if reports:  # 只有当有报告时才添加这个类型
            type_nav[type_names[report_type]] = reports
            reports_nav['报告'].append(type_nav)
    
    if reports_nav['报告']:  # 只有当有报告时才添加报告导航
        nav.append(reports_nav)
    
    return nav

def update_mkdocs_config():
    """更新 mkdocs.yml 文件中的导航配置"""
    config_path = os.path.join(PROJECT_ROOT, 'mkdocs.yml')
    
    # 读取现有配置
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"读取配置文件时出错: {e}")
        return False
    
    # 更新导航
    config['nav'] = generate_nav()
    
    # 写回配置文件
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True)
        logger.info("成功更新导航配置")
        return True
    except Exception as e:
        logger.error(f"写入配置文件时出错: {e}")
        return False

if __name__ == '__main__':
    update_mkdocs_config() 