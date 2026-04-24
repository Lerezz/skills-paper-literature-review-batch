# paper-literature-review-batch

## 功能简介
大批量论文文献综述自动生成工具，通过Subagent拆分任务解决上下文过载问题。支持输入研究目标与大批量PDF/zip论文包，自动生成合并后的文献综述文件。

## 核心优势
- **上下文过载解决**：通过Subagent拆分任务，避免大批量论文内容进入主Agent上下文
- **高效批量处理**：支持几十/上百篇论文的自动处理
- **规范输出格式**：统一生成符合学术规范的文献综述
- **自动清理**：处理完成后自动清理临时文件，仅保留最终成果

## 输入要求
- **研究目标**：明确的研究方向文本（用于指导论文分析）
- **论文文件**：单个/多个PDF文件，或包含大批量PDF的zip压缩包

## 执行流程
1. **文件处理**：调用file-handler-agent解压zip并将PDF转换为MD格式
2. **单篇分析**：批量调度paper-analyzer-agent对每篇论文进行独立分析
3. **综述合并**：收集所有单篇分析结果，合并为最终文献综述
4. **临时清理**：调用cleaner-agent清理临时文件

## 输出成果
- **最终文件**：`literature_review.md`（所有论文的综合文献综述）
- **进度反馈**：每一步任务完成后返回处理进度

## 目录结构
```
paper-literature-review-batch/
├── SKILL.md              # 技能主配置文件
├── sctips/
│   └── pdf_extract.py    # PDF转MD脚本
└── subagents/
    ├── cleaner-agent/    # 临时文件清理Subagent
    ├── file-handler-agent/ # 文件处理Subagent
    └── paper-analyzer-agent/ # 单篇论文分析Subagent
```

## 使用示例
```bash
# 处理单个PDF文件
python sctips/pdf_extract.py input.pdf output_dir

# 处理zip压缩包
python sctips/pdf_extract.py papers.zip output_dir
```

## 依赖环境
- Python 3.8+
- PyMuPDF (fitz)
- Git

## 许可证
MIT License