# check_sensitive_words
- 实现思路：jieba+pyahocorasick，先分词在判断分词结果中是否存在敏感词
- 特性：可以区分草和小草、牛奶和奶等case；但依赖于分词效果，一些较长的和特定事件会识别不到
- 可优化的思路：以上方案可以检测到通用的敏感词，在以上基础上，在此进行较长和特定事件的词库的检测，直接对原文使用iter_long来实现词的检测
