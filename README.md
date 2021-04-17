# PBRQ
该仓库是对<\<Search Me in the Dark: Privacy-preserving Boolean Range Query over Encrypted Spatial Data>\>论文的简单复现，由于对代码的理解不够深入，最终实现与论文源代码会存在很多出入，请酌情使用，同时也欢迎其他用户作出调整修改

文件结构：PBRQ2是对数据索引的实现，GrayCode用于生成格雷码表，tool用于读取数据，shve文件夹是SHVE加密的实现，test_data是测试数据，由于大小限制只截取了一部分

SHVE加密借鉴于https://github.com/shangqimonash/SHVE 伪随机函数采用ASE加密实现

最终测试结果结果只做了大小为1000的格雷表测试，之后扩大规模会带来很大的内存消耗，机器不支持

最后感谢原文作者在论文理解上的帮助
