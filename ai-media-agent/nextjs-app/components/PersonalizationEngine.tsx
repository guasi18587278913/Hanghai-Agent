// 个性化引擎 - 核心算法
export interface UserProfile {
  // 基础信息
  timeAvailable: number // 1-5 可用时间等级
  experience: number // 1-5 经验等级
  goal: 'income' | 'skill' | 'brand' | 'interest'
  
  // 学习偏好
  learningStyle: 'visual' | 'reading' | 'practice' | 'social'
  pace: 'fast' | 'moderate' | 'slow'
  contentPreference: string[]
  
  // 行为数据
  completedLessons: string[]
  currentStreak: number
  engagementScore: number
  weakPoints: string[]
  strongPoints: string[]
  
  // 个性化参数
  difficulty: number // 1-10
  motivationType: 'achievement' | 'social' | 'mastery' | 'purpose'
  preferredTime: 'morning' | 'afternoon' | 'evening' | 'night'
}

export class PersonalizationEngine {
  // 生成个性化学习路径
  static generatePath(profile: UserProfile) {
    const phases = []
    
    // 根据经验等级决定起点
    const startLevel = this.calculateStartLevel(profile)
    
    // 根据目标调整重点
    const focusAreas = this.determineFocusAreas(profile)
    
    // 根据学习风格定制内容形式
    const contentTypes = this.selectContentTypes(profile)
    
    // 根据可用时间安排强度
    const dailyTasks = this.calculateDailyLoad(profile)
    
    return {
      startLevel,
      focusAreas,
      contentTypes,
      dailyTasks,
      estimatedDuration: this.estimateDuration(profile),
      milestones: this.generateMilestones(profile)
    }
  }
  
  // 计算起始等级
  private static calculateStartLevel(profile: UserProfile): number {
    const weights = {
      experience: 0.4,
      timeAvailable: 0.2,
      engagementScore: 0.2,
      completedLessons: 0.2
    }
    
    return Math.round(
      profile.experience * weights.experience +
      profile.timeAvailable * weights.timeAvailable +
      (profile.engagementScore / 100) * 5 * weights.engagementScore +
      (profile.completedLessons.length / 10) * 5 * weights.completedLessons
    )
  }
  
  // 确定重点领域
  private static determineFocusAreas(profile: UserProfile): string[] {
    const focusMap = {
      income: ['变现策略', '商业合作', '流量运营'],
      skill: ['技术深度', '工具掌握', '创作能力'],
      brand: ['个人定位', '内容风格', '粉丝运营'],
      interest: ['探索尝试', '基础知识', '趣味案例']
    }
    
    return focusMap[profile.goal]
  }
  
  // 选择内容类型
  private static selectContentTypes(profile: UserProfile) {
    const contentMap = {
      visual: { video: 0.6, text: 0.2, interactive: 0.2 },
      reading: { video: 0.2, text: 0.6, interactive: 0.2 },
      practice: { video: 0.2, text: 0.2, interactive: 0.6 },
      social: { video: 0.3, text: 0.2, interactive: 0.5 }
    }
    
    return contentMap[profile.learningStyle]
  }
  
  // 计算每日负载
  private static calculateDailyLoad(profile: UserProfile) {
    const baseLoad: Record<number, { tasks: number; minutes: number }> = {
      1: { tasks: 1, minutes: 30 },
      2: { tasks: 2, minutes: 60 },
      3: { tasks: 3, minutes: 120 },
      4: { tasks: 4, minutes: 180 },
      5: { tasks: 5, minutes: 240 }
    }
    
    const load = baseLoad[profile.timeAvailable]
    
    // 根据学习节奏调整
    const paceMultiplier = {
      fast: 1.3,
      moderate: 1.0,
      slow: 0.7
    }
    
    return {
      tasks: Math.round(load.tasks * paceMultiplier[profile.pace]),
      minutes: Math.round(load.minutes * paceMultiplier[profile.pace])
    }
  }
  
  // 估算完成时间
  private static estimateDuration(profile: UserProfile): number {
    const baseDays = 21
    const experienceFactor = (6 - profile.experience) * 0.2
    const timeFactor = (6 - profile.timeAvailable) * 0.15
    
    return Math.round(baseDays * (1 + experienceFactor + timeFactor))
  }
  
  // 生成里程碑
  private static generateMilestones(profile: UserProfile) {
    const milestones = []
    
    if (profile.goal === 'income') {
      milestones.push(
        { day: 3, title: '完成第一个商业案例分析' },
        { day: 7, title: '发布10条带货内容' },
        { day: 14, title: '获得第一个商务合作' },
        { day: 21, title: '月收入突破5000' }
      )
    } else if (profile.goal === 'skill') {
      milestones.push(
        { day: 3, title: '掌握5个核心AI工具' },
        { day: 7, title: '完成第一个AI作品' },
        { day: 14, title: '形成个人工作流' },
        { day: 21, title: '独立完成复杂项目' }
      )
    }
    
    return milestones
  }
  
  // 动态调整难度
  static adjustDifficulty(profile: UserProfile, performance: number): number {
    const targetPerformance = 0.7 // 目标正确率70%
    const adjustmentRate = 0.1
    
    if (performance > targetPerformance + 0.1) {
      // 表现太好，增加难度
      return Math.min(10, profile.difficulty + adjustmentRate * 10)
    } else if (performance < targetPerformance - 0.1) {
      // 表现不佳，降低难度
      return Math.max(1, profile.difficulty - adjustmentRate * 10)
    }
    
    return profile.difficulty
  }
  
  // 推荐下一步内容
  static recommendNext(profile: UserProfile) {
    // 基于弱点推荐
    if (profile.weakPoints.length > 0) {
      return {
        type: 'improvement',
        content: `加强练习：${profile.weakPoints[0]}`,
        reason: '检测到薄弱环节'
      }
    }
    
    // 基于目标推荐
    if (profile.goal === 'income' && profile.completedLessons.length > 10) {
      return {
        type: 'practical',
        content: '开始接触真实商单',
        reason: '已具备基础，可以实战'
      }
    }
    
    // 默认推荐
    return {
      type: 'continue',
      content: '继续下一课',
      reason: '保持学习节奏'
    }
  }
}