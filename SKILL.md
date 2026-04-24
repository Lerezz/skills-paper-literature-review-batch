---
name: paper-literature-review-batch
description: 大批量论文文献综述自动生成（主Agent：调度Subagent，解决上下文过载）
version: 2.0.0
author: Trae User
agent:  # 主Agent配置：仅负责任务分发与结果汇总，不处理具体文本
  role: 任务调度专家
  goal: 协调3个Subagent，完成大批量论文的全流程处理，避免上下文堆积
  constraints: 不参与PDF提取、论文分析等具体文本操作，仅传递参数、接收结果
---

# 大批量文献综述自动生成（主Agent）
## 核心功能
接收：研究目标（文本）+ 大批量PDF/zip论文包（几十/上百篇）
输出：合并后的文献综述文件（literature_review.md），自动清理临时文件
核心优势：通过Subagent拆分任务，避免大批量论文内容进入主Agent上下文，解决过载问题

## 输入（必填）
- 研究目标：文本（明确研究方向，用于Subagent2的单篇分析）
- 论文文件：单个/多个PDF 文件，或 zip 压缩包（含大批量PDF）

## 执行流程（主Agent仅做调度，不处理具体内容）
1.  调用 Subagent：`file-handler-agent`，传递参数（论文文件、输出目录），获取处理完成的MD文件目录
2.  读取 MD 文件目录，批量调度 Subagent：`paper-analyzer-agent`，每篇MD单独调用（单篇处理，无上下文堆积）
3.  收集所有 Subagent2 输出的单篇综述，合并为最终文件 `literature_review.md`
4.  调用 Subagent：`cleaner-agent`，传递临时文件目录，完成清理
5.  输出最终文献综述文件，结束任务

## 输出
- 最终成果：`literature_review.md`（所有论文的综述合并版）
- 状态反馈：每一步任务完成后，返回进度（如“已处理10/50篇论文”）
- 清理结果：临时文件（解压PDF、提取MD）全部删除，仅保留最终文件

## 与Subagent交互规则
- 主Agent仅传递参数（不传递论文全文），Subagent处理完成后返回结果标识（如MD目录、单篇综述文本）
- 单篇论文分析采用“逐篇调用”模式，避免多篇论文内容同时进入上下文