'use client'

import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Sparkles, 
  Brain, 
  Target, 
  Rocket, 
  CheckCircle2,
  ArrowRight,
  User,
  Clock,
  Zap,
  BookOpen,
  TrendingUp,
  MessageCircle,
  Compass,
  Map,
  Anchor,
  Wind,
  Calendar,
  X
} from 'lucide-react'
import AIChatWidget from '../components/AIChatWidget'
import SmartAssessment from '../components/SmartAssessment'
import { PersonalizationEngine } from '../components/PersonalizationEngine'
import DetailedLearningPlan from '../components/DetailedLearningPlan'

export default function Home() {
  const [showLearningContent, setShowLearningContent] = useState(false)
  const [showSmartAssessment, setShowSmartAssessment] = useState(false)
  const [assessmentResult, setAssessmentResult] = useState<any>(null)
  const [showDetailedPlan, setShowDetailedPlan] = useState(false)


  const startLearning = () => {
    setShowLearningContent(true)
  }

  const handleAssessmentComplete = (result: any) => {
    setAssessmentResult(result)
    setShowSmartAssessment(false)
    setShowDetailedPlan(true)  // 直接跳转到21天计划
  }

  // 智能评测页面
  if (showSmartAssessment) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-teal-900 via-cyan-900 to-teal-900 p-4">
        <SmartAssessment onComplete={handleAssessmentComplete} />
        <AIChatWidget />
      </div>
    )
  }

  // 详细学习计划页面（测评完成后直接显示）
  if (showDetailedPlan) {
    return (
      <>
        <div className="min-h-screen bg-gradient-to-br from-teal-900 via-cyan-900 to-teal-900 p-4">
          <div className="max-w-6xl mx-auto">
            {!assessmentResult && (
              <button 
                onClick={() => setShowDetailedPlan(false)}
                className="mb-6 px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-colors flex items-center gap-2"
              >
                <ArrowRight className="w-4 h-4 rotate-180" />
                返回
              </button>
            )}
            <DetailedLearningPlan 
              currentDay={1} 
              assessmentResult={assessmentResult}
              onStartLearning={startLearning}
            />
          </div>
        </div>
        <AIChatWidget />
      </>
    )
  }

  // 学习内容页面
  if (showLearningContent) {
    return (
      <>
        <div className="min-h-screen bg-gradient-to-br from-teal-900 via-cyan-900 to-teal-900 p-4">
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="max-w-6xl mx-auto"
        >
          {/* 头部导航 */}
          <div className="flex items-center justify-between mb-8 glass-effect rounded-2xl p-4">
            <div className="flex items-center gap-3">
              <Anchor className="w-8 h-8 text-teal-300" />
              <h1 className="text-2xl font-bold text-white">AI自媒体航海手册</h1>
            </div>
            <button 
              onClick={() => setShowLearningContent(false)}
              className="px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-colors"
            >
              返回
            </button>
          </div>

          {/* 主要内容区 */}
          <div className="grid md:grid-cols-3 gap-6">
            {/* 左侧导航 */}
            <div className="md:col-span-1">
              <div className="glass-effect rounded-2xl p-6 sticky top-4">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <Map className="w-5 h-5 text-teal-300" />
                  学习路线
                </h3>
                <div className="space-y-3">
                  {[
                    { icon: <Compass />, title: "第一步：确定定位", status: "current" },
                    { icon: <Wind />, title: "第二步：账号搭建", status: "upcoming" },
                    { icon: <Anchor />, title: "第三步：内容发布", status: "upcoming" },
                    { icon: <Target />, title: "第四步：运营体系", status: "upcoming" }
                  ].map((item, i) => (
                    <div 
                      key={i}
                      className={`p-3 rounded-lg flex items-center gap-3 cursor-pointer transition-all ${
                        item.status === 'current' 
                          ? 'bg-teal-500/20 border border-teal-500/50' 
                          : 'hover:bg-white/5'
                      }`}
                    >
                      <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                        item.status === 'current' ? 'bg-teal-500' : 'bg-white/10'
                      }`}>
                        {React.cloneElement(item.icon, { 
                          className: `w-4 h-4 ${item.status === 'current' ? 'text-white' : 'text-gray-400'}` 
                        })}
                      </div>
                      <span className={item.status === 'current' ? 'text-white' : 'text-gray-400'}>
                        {item.title}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 右侧内容 */}
            <div className="md:col-span-2">
              <motion.div 
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                className="glass-effect rounded-2xl p-8"
              >
                <h2 className="text-3xl font-bold text-white mb-2">第一步：确定账号定位和方向</h2>
                <p className="text-teal-300 mb-6">找到适合自己的"AI+自媒体"方向</p>
                
                <div className="space-y-6 text-gray-200">
                  <div>
                    <h3 className="text-xl font-semibold text-white mb-3">什么是AI自媒体？</h3>
                    <p className="mb-4">
                      AI自媒体是指普及"AI相关知识"的内容账号。这类账号是真正的流量刺客，无论从点赞评论，还是接广告的数量都特别好。
                    </p>
                  </div>

                  <div>
                    <h3 className="text-xl font-semibold text-white mb-3">4大内容定位方向</h3>
                    <div className="space-y-4">
                      {[
                        {
                          title: "AI热点/技术解读",
                          desc: "给小白用户讲清楚复杂的AI概念，比如用通俗的比喻解释ChatGPT原理",
                          color: "from-blue-500 to-cyan-500"
                        },
                        {
                          title: "AI工具分享",
                          desc: "专注AI工具的测评和教程，比如Midjourney绘图教学、DeepSeek使用技巧",
                          color: "from-purple-500 to-pink-500"
                        },
                        {
                          title: "AI创业或副业",
                          desc: "分享AI相关的赚钱方式和案例分析，通过实际经验获得用户信任",
                          color: "from-orange-500 to-red-500"
                        },
                        {
                          title: "AI效率提升",
                          desc: "针对上班族和学生，分享提高效率的AI办公技巧",
                          color: "from-green-500 to-teal-500"
                        }
                      ].map((item, i) => (
                        <motion.div
                          key={i}
                          initial={{ x: -20, opacity: 0 }}
                          animate={{ x: 0, opacity: 1 }}
                          transition={{ delay: i * 0.1 }}
                          className="bg-white/5 rounded-xl p-5 border border-white/10 hover:bg-white/10 transition-colors"
                        >
                          <div className="flex items-start gap-4">
                            <div className={`w-2 h-full bg-gradient-to-b ${item.color} rounded-full`} />
                            <div className="flex-1">
                              <h4 className="font-semibold text-white mb-2">{item.title}</h4>
                              <p className="text-gray-300 text-sm">{item.desc}</p>
                            </div>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </div>

                  <div className="bg-teal-500/10 rounded-xl p-6 border border-teal-500/30">
                    <h4 className="text-lg font-semibold text-teal-300 mb-3">为什么现在还值得做？</h4>
                    <ul className="space-y-2">
                      <li className="flex items-start gap-2">
                        <CheckCircle2 className="w-5 h-5 text-teal-400 mt-0.5" />
                        <span>AI自媒体容易出爆款，20条内容可能出4-5条爆款</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <CheckCircle2 className="w-5 h-5 text-teal-400 mt-0.5" />
                        <span>广告主投放预算充足，头部玩家达亿元级别</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <CheckCircle2 className="w-5 h-5 text-teal-400 mt-0.5" />
                        <span>信息差战场，每天都有新机会</span>
                      </li>
                    </ul>
                  </div>

                  <div className="flex gap-4 mt-8">
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className="flex-1 px-6 py-3 bg-gradient-to-r from-teal-500 to-cyan-500 text-white font-semibold rounded-xl"
                    >
                      继续学习下一步
                    </motion.button>
                    <motion.a
                      href="https://scys.com/docx/Vuf1dbUNmoohFzxkICocLzblnCe"
                      target="_blank"
                      rel="noopener noreferrer"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className="px-6 py-3 bg-white/10 text-white font-semibold rounded-xl border border-white/20 inline-flex items-center gap-2"
                    >
                      <BookOpen className="w-5 h-5" />
                      查看完整手册
                    </motion.a>
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </motion.div>
        <AIChatWidget />
      </div>
      </>
    )
  }

  // 首页 - 默认显示
  if (!showSmartAssessment && !showDetailedPlan && !showLearningContent) {
    return (
      <>
        <div className="min-h-screen bg-gradient-to-br from-teal-900 via-cyan-900 to-teal-900 flex items-center justify-center p-4">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-4xl w-full"
        >
          {/* Hero Section */}
          <div className="text-center mb-12">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", duration: 0.5 }}
              className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-teal-500 to-cyan-500 rounded-2xl mb-6"
            >
              <Anchor className="w-10 h-10 text-white" />
            </motion.div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-4">
              AI自媒体
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-cyan-400">
                航海实战
              </span>
            </h1>
            
            <p className="text-xl text-gray-300 mb-8">
              航线已更新，等你一起下场实战
            </p>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            {[
              { icon: <Compass />, title: "智能导航", desc: "21天完整学习路径" },
              { icon: <Wind />, title: "实战手册", desc: "基于真实案例总结" },
              { icon: <Anchor />, title: "稳定起航", desc: "从0到1系统化教学" }
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="glass-effect rounded-2xl p-6 hover-lift"
              >
                <div className="w-12 h-12 bg-gradient-to-br from-teal-500 to-cyan-500 rounded-xl flex items-center justify-center mb-4">
                  {React.cloneElement(feature.icon, { className: "w-6 h-6 text-white" })}
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-gray-400">{feature.desc}</p>
              </motion.div>
            ))}
          </div>

          {/* CTA Button */}
          <motion.div className="text-center">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowSmartAssessment(true)}
              className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-teal-500 to-cyan-500 text-white font-semibold rounded-2xl hover:shadow-2xl transition-all">
              开始航海
              <ArrowRight className="ml-2 w-5 h-5" />
            </motion.button>
            
            <p className="text-gray-400 mt-4">
              已有 <span className="text-teal-400 font-semibold">2,380</span> 位圈友加入航海
            </p>
            
            <motion.a
              href="https://scys.com/docx/Vuf1dbUNmoohFzxkICocLzblnCe"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-4 text-teal-400 hover:text-teal-300 transition-colors text-sm"
            >
              📚 查看航海手册 →
            </motion.a>
          </motion.div>
        </motion.div>
        <AIChatWidget />
      </div>
      </>
    )
  }


}