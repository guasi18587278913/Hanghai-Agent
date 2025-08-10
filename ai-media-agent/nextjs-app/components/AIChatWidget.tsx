'use client'

import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  MessageCircle, 
  X, 
  Send, 
  Bot, 
  User,
  Sparkles,
  Book,
  TrendingUp,
  HelpCircle,
  Zap
} from 'lucide-react'

interface Message {
  id: string
  type: 'user' | 'ai'
  content: string
  timestamp: Date
  suggestions?: string[]
}

export default function AIChatWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'ai',
      content: '👋 你好！我是你的AI学习助手。我可以帮你：\n\n• 解答AI自媒体相关问题\n• 分析你的内容质量\n• 推荐学习资源\n• 制定个性化计划\n\n有什么可以帮助你的吗？',
      timestamp: new Date(),
      suggestions: ['如何快速涨粉？', '分析爆款案例', '今天该学什么？']
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const quickActions = [
    { icon: <Book className="w-4 h-4" />, label: '学习建议', query: '根据我的进度，今天应该学什么？' },
    { icon: <TrendingUp className="w-4 h-4" />, label: '内容分析', query: '帮我分析这个标题：AI改变生活的10种方式' },
    { icon: <HelpCircle className="w-4 h-4" />, label: '答疑解惑', query: '小红书和抖音哪个平台更适合新手？' },
    { icon: <Zap className="w-4 h-4" />, label: '爆款秘诀', query: '最近有什么AI热点可以蹭？' }
  ]

  const handleSend = async (message: string = inputValue) => {
    if (!message.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: message,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsTyping(true)

    // 模拟AI响应
    setTimeout(() => {
      const aiResponse = generateAIResponse(message)
      setMessages(prev => [...prev, aiResponse])
      setIsTyping(false)
    }, 1500)
  }

  const generateAIResponse = (query: string): Message => {
    const lowerQuery = query.toLowerCase()
    
    // 智能响应逻辑
    if (lowerQuery.includes('涨粉') || lowerQuery.includes('粉丝')) {
      return {
        id: Date.now().toString(),
        type: 'ai',
        content: '关于涨粉，我总结了几个核心要点：\n\n📈 **内容质量是根本**\n• 保持垂直度，让算法认识你\n• 前10秒要有钩子，留住用户\n• 标题要有信息差或情绪价值\n\n🎯 **发布策略**\n• 保持日更，建立用户预期\n• 选择用户活跃时段发布\n• 同一内容多平台分发\n\n💡 **互动运营**\n• 及时回复评论，提高互动率\n• 创造话题，引导用户讨论\n• 适当引导点赞收藏\n\n根据你目前的阶段，建议先专注内容质量，每天坚持发1-2条。',
        timestamp: new Date(),
        suggestions: ['查看爆款案例', '学习标题技巧', '了解平台规则']
      }
    }
    
    if (lowerQuery.includes('标题') || lowerQuery.includes('分析')) {
      return {
        id: Date.now().toString(),
        type: 'ai',
        content: '我来分析一下这个标题：\n\n📊 **标题评分：7.5/10**\n\n✅ **优点：**\n• 有数字"10"，增加具体感\n• "AI改变生活"是热门话题\n• 结构清晰，易于理解\n\n🔧 **优化建议：**\n• 加入时效性：2024年最新\n• 增加情绪点：普通人必看\n• 突出价值：月省3000元\n\n💡 **优化版本：**\n"2024普通人必看：AI改变生活的10个方法，月省3000元"\n\n这样改动后，点击率预计提升30%。',
        timestamp: new Date(),
        suggestions: ['更多标题模板', '爆款标题公式', '测试不同版本']
      }
    }
    
    if (lowerQuery.includes('今天') || lowerQuery.includes('学什么')) {
      return {
        id: Date.now().toString(),
        type: 'ai',
        content: '根据你的学习进度，今天的任务安排：\n\n📚 **上午（1小时）**\n• 学习课程：AI工具效率提升篇\n• 重点：ChatGPT高级技巧\n• 实践：完成3个prompt练习\n\n🎬 **下午（2小时）**\n• 内容创作：发布2条作品\n• 平台：小红书图文 + 抖音视频\n• 主题：分享今天学到的技巧\n\n📊 **晚上（30分钟）**\n• 数据复盘：分析昨天作品数据\n• 优化：根据反馈调整内容\n• 规划：明天的选题\n\n💪 加油！保持这个节奏，21天后你会看到明显进步。',
        timestamp: new Date(),
        suggestions: ['开始上午任务', '查看详细教程', '设置提醒']
      }
    }
    
    // 默认响应
    return {
      id: Date.now().toString(),
      type: 'ai',
      content: `我理解你的问题是关于"${query}"。\n\n让我为你提供一些建议：\n\n1. 首先，明确你的具体需求\n2. 然后，选择合适的学习路径\n3. 最后，坚持实践和优化\n\n你可以问我更具体的问题，比如：\n• 具体的操作步骤\n• 成功案例分析\n• 个性化建议`,
      timestamp: new Date(),
      suggestions: ['查看教程', '了解更多', '开始实践']
    }
  }

  return (
    <>
      {/* 悬浮按钮 */}
      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => setIsOpen(true)}
            className="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-full flex items-center justify-center shadow-lg z-50"
          >
            <MessageCircle className="w-6 h-6 text-white" />
            <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-pulse" />
          </motion.button>
        )}
      </AnimatePresence>

      {/* 聊天窗口 */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className="fixed bottom-6 right-6 w-96 h-[600px] bg-white rounded-2xl shadow-2xl z-50 flex flex-col overflow-hidden"
          >
            {/* 头部 */}
            <div className="bg-gradient-to-r from-teal-500 to-cyan-500 p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                  <Bot className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-white font-semibold">AI学习助手</h3>
                  <p className="text-white/80 text-xs">随时为你答疑解惑</p>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center hover:bg-white/30 transition-colors"
              >
                <X className="w-5 h-5 text-white" />
              </button>
            </div>

            {/* 快捷操作 */}
            <div className="p-3 bg-gray-50 border-b">
              <div className="flex gap-2 overflow-x-auto">
                {quickActions.map((action, i) => (
                  <button
                    key={i}
                    onClick={() => handleSend(action.query)}
                    className="flex items-center gap-1 px-3 py-1.5 bg-white rounded-lg border border-gray-200 hover:border-teal-500 hover:bg-teal-50 transition-colors whitespace-nowrap text-sm"
                  >
                    {action.icon}
                    <span>{action.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* 消息区域 */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`flex gap-2 max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.type === 'user' ? 'bg-teal-500' : 'bg-gray-200'
                    }`}>
                      {message.type === 'user' ? (
                        <User className="w-5 h-5 text-white" />
                      ) : (
                        <Sparkles className="w-5 h-5 text-gray-600" />
                      )}
                    </div>
                    <div>
                      <div className={`rounded-2xl px-4 py-2 ${
                        message.type === 'user' 
                          ? 'bg-teal-500 text-white' 
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        <p className="whitespace-pre-wrap text-sm">{message.content}</p>
                      </div>
                      {message.suggestions && (
                        <div className="mt-2 flex flex-wrap gap-2">
                          {message.suggestions.map((suggestion, i) => (
                            <button
                              key={i}
                              onClick={() => handleSend(suggestion)}
                              className="text-xs px-3 py-1 bg-white border border-gray-200 rounded-full hover:border-teal-500 hover:bg-teal-50 transition-colors"
                            >
                              {suggestion}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
              
              {isTyping && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex items-center gap-2"
                >
                  <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                    <Bot className="w-5 h-5 text-gray-600" />
                  </div>
                  <div className="bg-gray-100 rounded-2xl px-4 py-2">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                  </div>
                </motion.div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* 输入区域 */}
            <div className="p-4 border-t bg-white">
              <form onSubmit={(e) => { e.preventDefault(); handleSend() }} className="flex gap-2">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="输入你的问题..."
                  className="flex-1 px-4 py-2 border border-gray-200 rounded-full focus:outline-none focus:border-teal-500"
                />
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  type="submit"
                  className="w-10 h-10 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-full flex items-center justify-center text-white"
                >
                  <Send className="w-5 h-5" />
                </motion.button>
              </form>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}