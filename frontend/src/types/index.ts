export interface BasicInfo {
  name: string | null
  phone: string | null
  email: string | null
  address: string | null
}

export interface JobInfo {
  job_intention: string | null
  expected_salary: string | null
}

export interface BackgroundInfo {
  work_years: string | null
  education: string | null
  projects: string | null
}

export interface ResumeInfo {
  basic_info: BasicInfo
  job_info: JobInfo
  background_info: BackgroundInfo
}

export interface MatchScore {
  overall_score: number
  skill_match_rate: number
  content_similarity: number
  matched_keywords: string[]
}

export interface AnalysisResult {
  raw_text: string
  cleaned_text: string
  info: ResumeInfo
  match_score: MatchScore
}

export interface ApiResponse {
  success: boolean
  data?: AnalysisResult
  message?: string
}
