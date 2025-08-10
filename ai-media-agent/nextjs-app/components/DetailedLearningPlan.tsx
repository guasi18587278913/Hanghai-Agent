'use client'

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Calendar,
  CheckCircle2,
  Clock,
  Target,
  BookOpen,
  Video,
  Users,
  TrendingUp,
  Sparkles,
  ChevronDown,
  ChevronRight,
  Lock,
  Unlock,
  Star,
  X
} from 'lucide-react'

interface DayTask {
  day: number
  title: string
  tasks: string[]
  duration: string
  status: 'locked' | 'current' | 'completed'
  tips?: string
}

interface Phase {
  phase: number
  name: string
  description: string
  days: string
  color: string
  tasks: DayTask[]
}

const learningPlan: Phase[] = [
  {
    phase: 1,
    name: "定位阶段",
    description: "确定个人AI自媒体定位和方向",
    days: "第1-4天",
    color: "from-blue-500 to-cyan-500",
    tasks: [
      {
        day: 1,
        title: "研究对标账号(上)",
        tasks: [
          "搜索并关注5个AI领域头部账号",
          "记录每个账号的粉丝数、内容形式、更新频率",
          "分析他们的爆款内容特点（标题、封面、话题）",
          "建立对标账号分析表格"
        ],
        duration: "2-3小时",
        status: "current",
        tips: "重点关注小红书、抖音平台的AI创作者"
      },
      {
        day: 2,
        title: "研究对标账号(下)",
        tasks: [
          "再研究5个中腰部AI账号",
          "分析他们的成长路径和内容策略",
          "找出可直接借鉴的内容模板",
          "整理10个最受欢迎的选题方向"
        ],
        duration: "2-3小时",
        status: "locked",
        tips: "中腰部账号更容易模仿和超越"
      },
      {
        day: 3,
        title: "分析总结",
        tasks: [
          "总结3种最适合自己的内容形式",
          "确定2-3个细分赛道方向",
          "分析自己的优势和资源",
          "制定差异化策略"
        ],
        duration: "2小时",
        status: "locked"
      },
      {
        day: 4,
        title: "确定定位",
        tasks: [
          "最终确定账号定位和人设",
          "确定主攻平台（小红书/抖音/视频号）",
          "设计个人风格和内容调性",
          "写出100字的账号介绍"
        ],
        duration: "3小时",
        status: "locked",
        tips: "定位决定了后续所有内容方向"
      }
    ]
  },
  {
    phase: 2,
    name: "搭建阶段",
    description: "完成多平台账号注册和基础搭建",
    days: "第5-11天",
    color: "from-purple-500 to-pink-500",
    tasks: [
      {
        day: 5,
        title: "账号搭建",
        tasks: [
          "注册小红书、抖音账号",
          "设计并上传头像（使用AI生成）",
          "编写吸引人的账号简介",
          "完成基础认证和设置"
        ],
        duration: "2小时",
        status: "locked",
        tips: "头像和昵称要有辨识度"
      },
      {
        day: 6,
        title: "内容练习(图文)",
        tasks: [
          "模仿制作1条图文内容",
          "学习小红书排版技巧",
          "掌握封面图制作方法",
          "练习标题写作（10个）"
        ],
        duration: "3小时",
        status: "locked"
      },
      {
        day: 7,
        title: "内容练习(视频)",
        tasks: [
          "模仿制作1条短视频",
          "学习基础剪辑技巧",
          "练习口播表达能力",
          "了解平台算法规则"
        ],
        duration: "3小时",
        status: "locked"
      },
      {
        day: 8,
        title: "选题库搭建",
        tasks: [
          "收集20个热门AI话题",
          "建立选题灵感库",
          "分类整理（教程/资讯/工具/案例）",
          "规划首批10个选题"
        ],
        duration: "2小时",
        status: "locked"
      },
      {
        day: 9,
        title: "AI工具学习(文本)",
        tasks: [
          "深度学习ChatGPT/DeepSeek使用",
          "掌握10个实用prompt模板",
          "练习AI辅助写作",
          "整理AI工具使用心得"
        ],
        duration: "3小时",
        status: "locked",
        tips: "AI工具是内容创作的核心武器"
      },
      {
        day: 10,
        title: "AI工具学习(图像)",
        tasks: [
          "学习Midjourney/SD基础操作",
          "掌握图像生成prompt技巧",
          "制作10张不同风格的图片",
          "建立个人素材库"
        ],
        duration: "3小时",
        status: "locked"
      },
      {
        day: 11,
        title: "内容模板建立",
        tasks: [
          "设计3种内容模板",
          "确定发布时间策略",
          "制定内容生产SOP",
          "准备第一条正式内容"
        ],
        duration: "2小时",
        status: "locked"
      }
    ]
  },
  {
    phase: 3,
    name: "起号阶段",
    description: "持续发布作品，让账号打上标签",
    days: "第12-21天",
    color: "from-orange-500 to-red-500",
    tasks: [
      {
        day: 12,
        title: "首发作品",
        tasks: [
          "精心打磨第1条内容",
          "优化标题和封面",
          "选择最佳发布时间",
          "发布并观察数据"
        ],
        duration: "3小时",
        status: "locked",
        tips: "第一条内容决定账号起步"
      },
      {
        day: 13,
        title: "第2条内容",
        tasks: [
          "分析首发数据反馈",
          "调整优化第2条内容",
          "测试不同话题方向",
          "积极回复评论互动"
        ],
        duration: "2小时",
        status: "locked"
      },
      {
        day: 14,
        title: "日更开始",
        tasks: [
          "发布第3-4条内容",
          "建立日更节奏",
          "优化内容生产流程",
          "开始建立粉丝群"
        ],
        duration: "2小时",
        status: "locked"
      },
      {
        day: 15,
        title: "内容优化",
        tasks: [
          "发布第5-6条内容",
          "分析哪类内容数据好",
          "调整内容策略",
          "尝试蹭热点话题"
        ],
        duration: "2小时",
        status: "locked"
      },
      {
        day: 16,
        title: "爆款尝试",
        tasks: [
          "发布第7-8条内容",
          "模仿爆款结构创作",
          "优化关键词和标签",
          "增加互动环节设计"
        ],
        duration: "2小时",
        status: "locked",
        tips: "持续发布让算法认识你"
      },
      {
        day: 17,
        title: "稳定输出",
        tasks: [
          "发布第9-10条内容",
          "总结前期经验教训",
          "固定内容发布节奏",
          "开始跨平台分发"
        ],
        duration: "2小时",
        status: "locked"
      },
      {
        day: 18,
        title: "系列化内容",
        tasks: [
          "策划一个系列选题",
          "制作系列第1期",
          "设计系列视觉风格",
          "预告下期内容"
        ],
        duration: "3小时",
        status: "locked"
      },
      {
        day: 19,
        title: "数据复盘",
        tasks: [
          "分析10条内容数据",
          "找出爆款规律",
          "优化后续选题",
          "制定下周计划"
        ],
        duration: "2小时",
        status: "locked"
      },
      {
        day: 20,
        title: "变现准备",
        tasks: [
          "了解平台变现规则",
          "开通创作者权益",
          "准备商务合作资料",
          "设计知识付费产品"
        ],
        duration: "2小时",
        status: "locked",
        tips: "为后续变现做准备"
      },
      {
        day: 21,
        title: "阶段总结",
        tasks: [
          "总结21天成果",
          "制定下阶段目标",
          "优化运营策略",
          "庆祝完成挑战！"
        ],
        duration: "2小时",
        status: "locked"
      }
    ]
  }
]

interface DetailedLearningPlanProps {
  currentDay?: number
  assessmentResult?: any
  onStartLearning?: () => void
}

export default function DetailedLearningPlan({ 
  currentDay = 1, 
  assessmentResult,
  onStartLearning 
}: DetailedLearningPlanProps) {
  const [expandedPhase, setExpandedPhase] = useState<number | null>(0)
  const [selectedDay, setSelectedDay] = useState<DayTask | null>(null)

  const getTaskStatus = (day: number): 'completed' | 'current' | 'locked' => {
    if (day < currentDay) return 'completed'
    if (day === currentDay) return 'current'
    return 'locked'
  }

  const updateTaskStatuses = () => {
    return learningPlan.map(phase => ({
      ...phase,
      tasks: phase.tasks.map(task => ({
        ...task,
        status: getTaskStatus(task.day) as 'completed' | 'current' | 'locked'
      }))
    }))
  }

  const updatedPlan = updateTaskStatuses()

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* 总览 */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-3xl font-bold text-white">21天学习计划</h2>
          <div className="flex gap-3">
            <motion.a
              href="https://scys.com/docx/Vuf1dbUNmoohFzxkICocLzblnCe"
              target="_blank"
              rel="noopener noreferrer"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-colors flex items-center gap-2"
            >
              <BookOpen className="w-4 h-4" />
              查看手册
            </motion.a>
            {onStartLearning && (
              <motion.button
                onClick={onStartLearning}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-4 py-2 bg-gradient-to-r from-teal-500 to-cyan-500 text-white rounded-lg flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                开始学习
              </motion.button>
            )}
          </div>
        </div>
        
        <div className="flex items-center gap-4 text-gray-300">
          <div className="flex items-center gap-2">
            <Calendar className="w-5 h-5 text-teal-400" />
            <span>当前进度：第 {currentDay} 天</span>
          </div>
          <div className="flex items-center gap-2">
            <Target className="w-5 h-5 text-teal-400" />
            <span>完成度：{Math.round((currentDay / 21) * 100)}%</span>
          </div>
        </div>
        
        {/* 进度条 */}
        <div className="mt-4 h-3 bg-white/10 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${(currentDay / 21) * 100}%` }}
            transition={{ duration: 1 }}
            className="h-full bg-gradient-to-r from-teal-500 to-cyan-500"
          />
        </div>
        
        {/* 个性化推荐信息 */}
        {assessmentResult && (
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="mt-6 glass-effect rounded-xl p-4"
          >
            <h4 className="text-lg font-semibold text-white mb-3">你的个性化学习方案</h4>
            <div className="grid md:grid-cols-3 gap-4 text-sm">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-teal-400" />
                <span className="text-gray-300">
                  每天学习 <span className="text-teal-400 font-semibold">{assessmentResult.learningPath.dailyTime}分钟</span>
                </span>
              </div>
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-teal-400" />
                <span className="text-gray-300">
                  推荐平台：<span className="text-teal-400 font-semibold">{assessmentResult.contentStrategy.platforms.join('、')}</span>
                </span>
              </div>
              <div className="flex items-center gap-2">
                <Star className="w-4 h-4 text-teal-400" />
                <span className="text-gray-300">
                  变现潜力：<span className="text-yellow-400">{'⭐'.repeat(assessmentResult.monetization.potential)}</span>
                </span>
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {/* 阶段列表 */}
      <div className="space-y-6">
        {updatedPlan.map((phase, phaseIndex) => (
          <motion.div
            key={phase.phase}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: phaseIndex * 0.1 }}
            className="glass-effect rounded-2xl overflow-hidden"
          >
            {/* 阶段头部 */}
            <button
              onClick={() => setExpandedPhase(expandedPhase === phaseIndex ? null : phaseIndex)}
              className="w-full p-6 flex items-center justify-between hover:bg-white/5 transition-colors"
            >
              <div className="flex items-center gap-4">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${phase.color} flex items-center justify-center`}>
                  <span className="text-white font-bold text-lg">{phase.phase}</span>
                </div>
                <div className="text-left">
                  <h3 className="text-xl font-semibold text-white">{phase.name}</h3>
                  <p className="text-gray-400 text-sm mt-1">{phase.description}</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-teal-400 text-sm">{phase.days}</span>
                {expandedPhase === phaseIndex ? (
                  <ChevronDown className="w-5 h-5 text-gray-400" />
                ) : (
                  <ChevronRight className="w-5 h-5 text-gray-400" />
                )}
              </div>
            </button>

            {/* 阶段内容 */}
            <AnimatePresence>
              {expandedPhase === phaseIndex && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  className="border-t border-white/10"
                >
                  <div className="p-6 grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {phase.tasks.map((task) => (
                      <motion.button
                        key={task.day}
                        whileHover={{ scale: task.status !== 'locked' ? 1.02 : 1 }}
                        whileTap={{ scale: task.status !== 'locked' ? 0.98 : 1 }}
                        onClick={() => task.status !== 'locked' && setSelectedDay(task)}
                        className={`p-4 rounded-xl border transition-all text-left ${
                          task.status === 'completed' 
                            ? 'bg-teal-500/10 border-teal-500/30 cursor-pointer'
                            : task.status === 'current'
                            ? 'bg-cyan-500/20 border-cyan-500 cursor-pointer animate-pulse'
                            : 'bg-white/5 border-white/10 cursor-not-allowed opacity-50'
                        }`}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <span className="text-gray-400 text-sm">Day</span>
                            <span className="text-white font-bold">{task.day}</span>
                          </div>
                          {task.status === 'completed' ? (
                            <CheckCircle2 className="w-5 h-5 text-teal-400" />
                          ) : task.status === 'current' ? (
                            <Sparkles className="w-5 h-5 text-cyan-400" />
                          ) : (
                            <Lock className="w-5 h-5 text-gray-500" />
                          )}
                        </div>
                        <h4 className="text-white font-medium mb-2">{task.title}</h4>
                        <div className="flex items-center gap-2 text-xs text-gray-400">
                          <Clock className="w-3 h-3" />
                          <span>{task.duration}</span>
                        </div>
                        {task.tips && (
                          <div className="mt-2 text-xs text-teal-400 line-clamp-1">
                            💡 {task.tips}
                          </div>
                        )}
                      </motion.button>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        ))}
      </div>

      {/* 详细任务弹窗 */}
      <AnimatePresence>
        {selectedDay && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setSelectedDay(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-gradient-to-br from-teal-900 to-cyan-900 rounded-2xl p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-2xl font-bold text-white">Day {selectedDay.day}: {selectedDay.title}</h3>
                  <p className="text-gray-400 mt-1">预计用时：{selectedDay.duration}</p>
                </div>
                <button
                  onClick={() => setSelectedDay(null)}
                  className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-white/20 transition-colors"
                >
                  <X className="w-5 h-5 text-white" />
                </button>
              </div>

              <div className="space-y-3">
                <h4 className="text-lg font-semibold text-teal-400">今日任务清单</h4>
                {selectedDay.tasks.map((task, index) => (
                  <div
                    key={index}
                    className="flex items-start gap-3 p-3 bg-white/5 rounded-lg"
                  >
                    <div className="w-6 h-6 bg-teal-500/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-teal-400 text-xs">{index + 1}</span>
                    </div>
                    <p className="text-gray-300">{task}</p>
                  </div>
                ))}
              </div>

              {selectedDay.tips && (
                <div className="mt-6 p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
                  <div className="flex items-start gap-2">
                    <Star className="w-5 h-5 text-yellow-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <h5 className="text-yellow-400 font-medium mb-1">学习建议</h5>
                      <p className="text-gray-300 text-sm">{selectedDay.tips}</p>
                    </div>
                  </div>
                </div>
              )}

              {selectedDay.status === 'current' && (
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="mt-6 w-full py-3 bg-gradient-to-r from-teal-500 to-cyan-500 text-white font-semibold rounded-xl"
                >
                  标记为已完成
                </motion.button>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}