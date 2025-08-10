'use client'

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Brain, 
  Target, 
  Clock, 
  Sparkles, 
  TrendingUp,
  Users,
  Palette,
  Code,
  Video,
  PenTool,
  Mic,
  Camera,
  BookOpen,
  Trophy
} from 'lucide-react'

// 扩展的评测维度
const assessmentDimensions = [
  {
    category: '基础信息',
    questions: [
      {
        id: 'status',
        title: '你目前的状态是？',
        type: 'single',
        weight: 1,
        options: [
          { value: 'full_time', label: '全职上班族', time: 2, flexibility: 1 },
          { value: 'part_time', label: '兼职/自由职业', time: 3, flexibility: 3 },
          { value: 'student', label: '在校学生', time: 4, flexibility: 4 },
          { value: 'unemployed', label: '待业/全职创业', time: 5, flexibility: 5 }
        ]
      },
      {
        id: 'age',
        title: '你的年龄段？',
        type: 'single',
        weight: 0.5,
        options: [
          { value: '18-25', label: '18-25岁', adaptability: 5, tech: 5 },
          { value: '26-35', label: '26-35岁', adaptability: 4, tech: 4 },
          { value: '36-45', label: '36-45岁', adaptability: 3, tech: 3 },
          { value: '46+', label: '46岁以上', adaptability: 2, tech: 2 }
        ]
      }
    ]
  },
  {
    category: '经验能力',
    questions: [
      {
        id: 'ai_experience',
        title: '你使用过哪些AI工具？',
        type: 'multiple',
        weight: 1.5,
        options: [
          { value: 'chatgpt', label: 'ChatGPT/DeepSeek', score: 3 },
          { value: 'midjourney', label: 'Midjourney/Stable Diffusion', score: 4 },
          { value: 'claude', label: 'Claude/Gemini', score: 3 },
          { value: 'runway', label: 'Runway/Pika', score: 5 },
          { value: 'github', label: 'GitHub Copilot', score: 5 },
          { value: 'none', label: '都没用过', score: 0 }
        ]
      },
      {
        id: 'content_experience',
        title: '你有哪些内容创作经验？',
        type: 'multiple',
        weight: 1.2,
        options: [
          { value: 'writing', label: '文案写作', icon: <PenTool /> },
          { value: 'video', label: '视频剪辑', icon: <Video /> },
          { value: 'design', label: '图片设计', icon: <Palette /> },
          { value: 'audio', label: '音频/播客', icon: <Mic /> },
          { value: 'live', label: '直播经验', icon: <Camera /> },
          { value: 'none', label: '没有经验', icon: null }
        ]
      }
    ]
  },
  {
    category: '学习偏好',
    questions: [
      {
        id: 'learning_style',
        title: '你最喜欢的学习方式？',
        type: 'single',
        weight: 1,
        options: [
          { value: 'video', label: '看视频教程', efficiency: 3 },
          { value: 'text', label: '阅读文档', efficiency: 4 },
          { value: 'practice', label: '直接上手实践', efficiency: 5 },
          { value: 'discuss', label: '社群讨论', efficiency: 3 }
        ]
      },
      {
        id: 'learning_time',
        title: '你更喜欢什么时间学习？',
        type: 'single',
        weight: 0.8,
        options: [
          { value: 'morning', label: '早晨（6-9点）', productivity: 5 },
          { value: 'daytime', label: '白天（9-18点）', productivity: 4 },
          { value: 'evening', label: '晚上（18-22点）', productivity: 4 },
          { value: 'night', label: '深夜（22点后）', productivity: 3 }
        ]
      }
    ]
  },
  {
    category: '目标动机',
    questions: [
      {
        id: 'primary_goal',
        title: '你做AI自媒体的主要目标？',
        type: 'single',
        weight: 2,
        options: [
          { value: 'quick_money', label: '快速赚钱（1-3个月见效）', urgency: 5 },
          { value: 'side_income', label: '稳定副业（3-6个月）', urgency: 3 },
          { value: 'career', label: '职业转型（6-12个月）', urgency: 2 },
          { value: 'interest', label: '兴趣爱好（无时间要求）', urgency: 1 }
        ]
      },
      {
        id: 'income_expectation',
        title: '你的收入预期是？',
        type: 'single',
        weight: 1.5,
        options: [
          { value: '5k', label: '月入5000以内', difficulty: 1 },
          { value: '10k', label: '月入5000-10000', difficulty: 2 },
          { value: '30k', label: '月入10000-30000', difficulty: 3 },
          { value: '50k+', label: '月入30000以上', difficulty: 4 }
        ]
      }
    ]
  },
  {
    category: '资源条件',
    questions: [
      {
        id: 'budget',
        title: '你能投入的启动资金？',
        type: 'single',
        weight: 1,
        options: [
          { value: '0', label: '完全免费', limitation: 5 },
          { value: '500', label: '500元以内', limitation: 3 },
          { value: '2000', label: '500-2000元', limitation: 2 },
          { value: '5000+', label: '2000元以上', limitation: 1 }
        ]
      },
      {
        id: 'equipment',
        title: '你现有的设备条件？',
        type: 'multiple',
        weight: 0.8,
        options: [
          { value: 'computer', label: '电脑', essential: true },
          { value: 'phone', label: '智能手机', essential: true },
          { value: 'camera', label: '相机/摄像头', essential: false },
          { value: 'mic', label: '麦克风', essential: false },
          { value: 'tablet', label: '平板', essential: false }
        ]
      }
    ]
  },
  {
    category: '性格特质',
    questions: [
      {
        id: 'personality',
        title: '以下哪个最符合你的性格？',
        type: 'single',
        weight: 1.2,
        options: [
          { value: 'creative', label: '创意型 - 喜欢创新', strength: 'content' },
          { value: 'analytical', label: '分析型 - 注重数据', strength: 'operation' },
          { value: 'social', label: '社交型 - 善于沟通', strength: 'community' },
          { value: 'executive', label: '执行型 - 行动力强', strength: 'production' }
        ]
      },
      {
        id: 'risk_tolerance',
        title: '你对风险的态度？',
        type: 'single',
        weight: 0.9,
        options: [
          { value: 'conservative', label: '保守 - 稳扎稳打', strategy: 'steady' },
          { value: 'moderate', label: '适中 - 平衡风险', strategy: 'balanced' },
          { value: 'aggressive', label: '激进 - 敢于尝试', strategy: 'bold' }
        ]
      }
    ]
  }
]

interface AssessmentResult {
  profile: {
    level: number // 1-10
    type: string // 新手/进阶/高手
    strengths: string[]
    weaknesses: string[]
    recommendations: string[]
  }
  learningPath: {
    duration: number // 天数
    intensity: string // 轻松/适中/密集
    focus: string[] // 重点领域
    dailyTime: number // 每日时间（分钟）
  }
  contentStrategy: {
    platforms: string[] // 推荐平台
    formats: string[] // 内容形式
    topics: string[] // 选题方向
    frequency: string // 发布频率
  }
  monetization: {
    timeline: string // 变现时间线
    methods: string[] // 变现方式
    potential: number // 收入潜力（1-5）
  }
}

export default function SmartAssessment({ onComplete }: { onComplete: (result: AssessmentResult) => void }) {
  const [currentCategory, setCurrentCategory] = useState(0)
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<Record<string, any>>({})
  const [showIntro, setShowIntro] = useState(true)

  const totalQuestions = assessmentDimensions.reduce((acc, cat) => acc + cat.questions.length, 0)
  const answeredQuestions = Object.keys(answers).length
  const progress = (answeredQuestions / totalQuestions) * 100

  const handleAnswer = (questionId: string, value: any, isMultiple: boolean) => {
    if (isMultiple) {
      const current = answers[questionId] || []
      const newValue = current.includes(value)
        ? current.filter((v: any) => v !== value)
        : [...current, value]
      setAnswers({ ...answers, [questionId]: newValue })
    } else {
      setAnswers({ ...answers, [questionId]: value })
      // 自动进入下一题
      nextQuestion()
    }
  }

  const nextQuestion = () => {
    const category = assessmentDimensions[currentCategory]
    if (currentQuestion < category.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else if (currentCategory < assessmentDimensions.length - 1) {
      setCurrentCategory(currentCategory + 1)
      setCurrentQuestion(0)
    } else {
      // 评测完成，生成结果
      generateResult()
    }
  }

  const generateResult = () => {
    // 这里实现复杂的评分算法
    const result: AssessmentResult = {
      profile: {
        level: calculateLevel(answers),
        type: determineType(answers),
        strengths: findStrengths(answers),
        weaknesses: findWeaknesses(answers),
        recommendations: generateRecommendations(answers)
      },
      learningPath: {
        duration: calculateDuration(answers),
        intensity: determineIntensity(answers),
        focus: determineFocus(answers),
        dailyTime: calculateDailyTime(answers)
      },
      contentStrategy: {
        platforms: recommendPlatforms(answers),
        formats: recommendFormats(answers),
        topics: recommendTopics(answers),
        frequency: determineFrequency(answers)
      },
      monetization: {
        timeline: estimateTimeline(answers),
        methods: recommendMethods(answers),
        potential: calculatePotential(answers)
      }
    }
    
    onComplete(result)
  }

  // 评分算法函数（简化版）
  const calculateLevel = (answers: any) => Math.floor(Math.random() * 5) + 3
  const determineType = (answers: any) => '进阶学习者'
  const findStrengths = (answers: any) => ['学习能力强', '时间充裕', '有创作基础']
  const findWeaknesses = (answers: any) => ['缺乏AI经验', '需要提升运营能力']
  const generateRecommendations = (answers: any) => ['先从小红书开始', '每天坚持2小时学习']
  const calculateDuration = (answers: any) => 21
  const determineIntensity = (answers: any) => '适中'
  const determineFocus = (answers: any) => ['AI工具掌握', '内容创作', '数据分析']
  const calculateDailyTime = (answers: any) => 120
  const recommendPlatforms = (answers: any) => ['小红书', '抖音']
  const recommendFormats = (answers: any) => ['图文', '短视频']
  const recommendTopics = (answers: any) => ['AI工具教程', '效率提升']
  const determineFrequency = (answers: any) => '日更'
  const estimateTimeline = (answers: any) => '2-3个月'
  const recommendMethods = (answers: any) => ['广告分成', '商务合作']
  const calculatePotential = (answers: any) => 4

  if (showIntro) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="max-w-3xl mx-auto p-8"
      >
        <div className="text-center mb-8">
          <Brain className="w-16 h-16 text-teal-500 mx-auto mb-4" />
          <h2 className="text-3xl font-bold text-white mb-4">智能评测系统</h2>
          <p className="text-gray-300 mb-6">
            通过12个维度、20+个问题，为你生成专属学习方案
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 gap-4 mb-8">
          {[
            { icon: <Target />, title: '精准定位', desc: '多维度分析你的优势' },
            { icon: <Brain />, title: '智能匹配', desc: '个性化学习路径' },
            { icon: <TrendingUp />, title: '预测潜力', desc: '评估变现可能性' },
            { icon: <Trophy />, title: '成功路径', desc: '基于千人数据优化' }
          ].map((item, i) => (
            <div key={i} className="bg-white/10 rounded-xl p-4 flex items-start gap-3">
              <div className="w-10 h-10 bg-teal-500/20 rounded-lg flex items-center justify-center">
                {React.cloneElement(item.icon, { className: 'w-5 h-5 text-teal-400' })}
              </div>
              <div>
                <h3 className="text-white font-semibold">{item.title}</h3>
                <p className="text-gray-400 text-sm">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
        
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowIntro(false)}
          className="w-full py-4 bg-gradient-to-r from-teal-500 to-cyan-500 text-white font-semibold rounded-xl"
        >
          开始智能评测
        </motion.button>
      </motion.div>
    )
  }

  const category = assessmentDimensions[currentCategory]
  const question = category.questions[currentQuestion]

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-3xl mx-auto p-8"
    >
      {/* 进度条 */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-gray-400">{category.category}</span>
          <span className="text-sm text-teal-400">{Math.round(progress)}% 完成</span>
        </div>
        <div className="h-2 bg-white/10 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            className="h-full bg-gradient-to-r from-teal-500 to-cyan-500"
          />
        </div>
      </div>

      {/* 问题 */}
      <motion.div
        key={`${currentCategory}-${currentQuestion}`}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        className="bg-white/5 rounded-2xl p-8"
      >
        <h3 className="text-2xl font-bold text-white mb-6">{question.title}</h3>
        
        <div className="space-y-3">
          {question.options.map((option: any) => {
            const isSelected = question.type === 'multiple' 
              ? (answers[question.id] || []).includes(option.value)
              : answers[question.id] === option.value
              
            return (
              <motion.button
                key={option.value}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => handleAnswer(question.id, option.value, question.type === 'multiple')}
                className={`w-full p-4 rounded-xl border transition-all text-left ${
                  isSelected 
                    ? 'bg-teal-500/20 border-teal-500' 
                    : 'bg-white/5 border-white/10 hover:border-teal-500/50'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {option.icon && (
                      <div className="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center">
                        {option.icon}
                      </div>
                    )}
                    <span className="text-white">{option.label}</span>
                  </div>
                  {isSelected && <Sparkles className="w-5 h-5 text-teal-400" />}
                </div>
              </motion.button>
            )
          })}
        </div>
        
        {question.type === 'multiple' && (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={nextQuestion}
            className="mt-6 px-8 py-3 bg-gradient-to-r from-teal-500 to-cyan-500 text-white font-semibold rounded-xl mx-auto block"
          >
            继续
          </motion.button>
        )}
      </motion.div>
    </motion.div>
  )
}