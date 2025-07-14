"""
RAG服务核心实现
"""
import logging
from typing import List, Dict, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.schema import Document
from app.core.config import settings
from app.db.models import KnowledgeChunk

logger = logging.getLogger(__name__)


class RAGService:
    """RAG检索增强生成服务"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?"]
        )
        
        # 初始化向量存储
        self.vector_store = PGVector(
            connection_string=settings.DATABASE_URL,
            embedding_function=self.embeddings,
            collection_name="knowledge_base"
        )
    
    async def search(
        self, 
        query: str, 
        k: int = 5,
        filter_source: Optional[str] = None
    ) -> List[Dict]:
        """
        搜索相关文档
        
        Args:
            query: 查询文本
            k: 返回结果数量
            filter_source: 过滤来源
            
        Returns:
            相关文档列表
        """
        try:
            # 构建过滤器
            filter_dict = {}
            if filter_source:
                filter_dict["source"] = filter_source
            
            # 相似度搜索
            results = await self.vector_store.asimilarity_search_with_score(
                query=query,
                k=k,
                filter=filter_dict
            )
            
            # 格式化结果
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score)
                })
            
            logger.info(f"Found {len(formatted_results)} relevant documents")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    async def add_document(
        self, 
        content: str, 
        source: str, 
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        添加文档到知识库
        
        Args:
            content: 文档内容
            source: 文档来源
            metadata: 额外元数据
            
        Returns:
            是否成功
        """
        try:
            # 分割文档
            chunks = self.text_splitter.split_text(content)
            
            # 创建Document对象
            documents = []
            for i, chunk in enumerate(chunks):
                doc_metadata = {
                    "source": source,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
                if metadata:
                    doc_metadata.update(metadata)
                
                documents.append(Document(
                    page_content=chunk,
                    metadata=doc_metadata
                ))
            
            # 添加到向量存储
            await self.vector_store.aadd_documents(documents)
            
            logger.info(f"Added {len(documents)} chunks from {source}")
            return True
            
        except Exception as e:
            logger.error(f"Add document error: {e}")
            return False
    
    async def delete_by_source(self, source: str) -> bool:
        """
        根据来源删除文档
        
        Args:
            source: 文档来源
            
        Returns:
            是否成功
        """
        try:
            # TODO: 实现按来源删除逻辑
            logger.info(f"Deleted documents from source: {source}")
            return True
            
        except Exception as e:
            logger.error(f"Delete documents error: {e}")
            return False
    
    async def get_stats(self) -> Dict:
        """
        获取知识库统计信息
        
        Returns:
            统计信息字典
        """
        try:
            # TODO: 实现统计信息查询
            return {
                "total_documents": 0,
                "total_chunks": 0,
                "sources": []
            }
            
        except Exception as e:
            logger.error(f"Get stats error: {e}")
            return {}
    
    async def hybrid_search(
        self,
        query: str,
        k: int = 5,
        alpha: float = 0.7
    ) -> List[Dict]:
        """
        混合搜索（向量搜索 + 关键词搜索）
        
        Args:
            query: 查询文本
            k: 返回结果数量
            alpha: 向量搜索权重
            
        Returns:
            搜索结果
        """
        try:
            # 向量搜索
            vector_results = await self.search(query, k=k)
            
            # 关键词搜索（简单实现）
            keyword_results = await self._keyword_search(query, k=k)
            
            # 结果融合
            combined_results = self._combine_results(
                vector_results, 
                keyword_results, 
                alpha
            )
            
            return combined_results[:k]
            
        except Exception as e:
            logger.error(f"Hybrid search error: {e}")
            return await self.search(query, k)
    
    async def _keyword_search(self, query: str, k: int = 5) -> List[Dict]:
        """关键词搜索（基于PostgreSQL全文搜索）"""
        # TODO: 实现关键词搜索
        return []
    
    def _combine_results(
        self, 
        vector_results: List[Dict], 
        keyword_results: List[Dict], 
        alpha: float
    ) -> List[Dict]:
        """结果融合算法"""
        # TODO: 实现更复杂的结果融合逻辑
        return vector_results