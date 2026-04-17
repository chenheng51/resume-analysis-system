import jieba
from typing import Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ResumeMatcher:
    @staticmethod
    def extract_keywords(text: str) -> list:
        words = jieba.lcut(text)
        stopwords = {'的', '了', '和', '是', '就', '都', '而', '及', '与', '在', '对', '等', '有', '也', '很'}
        return [word for word in words if word not in stopwords and len(word) > 1]

    @classmethod
    def calculate_match_score(cls, resume_text: str, job_requirement: str) -> Dict[str, Any]:
        resume_keywords = cls.extract_keywords(resume_text)
        job_keywords = cls.extract_keywords(job_requirement)

        common_keywords = set(resume_keywords) & set(job_keywords)
        skill_match_rate = len(common_keywords) / len(job_keywords) if job_keywords else 0

        documents = [resume_text, job_requirement]
        tfidf = TfidfVectorizer()
        try:
            tfidf_matrix = tfidf.fit_transform(documents)
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except:
            cosine_sim = 0

        overall_score = (skill_match_rate * 0.6 + cosine_sim * 0.4) * 100

        return {
            "overall_score": round(overall_score, 2),
            "skill_match_rate": round(skill_match_rate * 100, 2),
            "content_similarity": round(cosine_sim * 100, 2),
            "matched_keywords": list(common_keywords)[:20]
        }
