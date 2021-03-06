# coding:utf-8
#! /usr/bin/env python

import os

import numpy as np

import data_helpers
import tensorflow as tf
from tensorflow.contrib import learn

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")
# 填写训练获得模型的存储位置
tf.flags.DEFINE_string("checkpoint_dir", "./runs/1553949706/checkpoints", "Checkpoint directory from training run")
tf.flags.DEFINE_string("test_data", "./fenci1/testData.txt", "Data source for the positive data.")

FLAGS = tf.flags.FLAGS

checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
# saver = tf.train.Saver()  # defaults to saving all variables
isTrain = False
graph = tf.Graph()

x_raw, y_test = data_helpers.load_test_data(FLAGS.test_data)
# word = u"标 题: 英特尔大力投资互联网设备公司 发信站: 日月光华站 (Tue Nov 30 14:09:10 1999) , 转信 　　英特尔，这家靠PC起家而雄霸天下的世界最大半导体生产商，把它的触角伸向PC以 外的世界，这早已不是什么秘密了。然而英特尔把它庞大的风险资本投向PC以外的计算 机公司，这可有点新鲜。 　　英特尔把它的48亿美元风险基金及其对其他300多家公司的投资都集中投向新一代互 联网网络设备生产及网络公司的发展方面。事实上，到十月中旬，它已达成了150多项协 议，英特尔希望到1999年年底，它的投资金额能超过去年的800,000,000美元。 　　有它每轮10,000,000美元的多轮投资额度，英特尔足以使那些新技术公司蓬勃发展 。事实上，这家拥有1 00多名员工的公司，业已成为世界上最大的风险资本投资公司， 所以它的投资战略足以影响世界高科技市场的走向。英特尔公司业务发展部主任Leslie Vadasz说：“我们总是问自己，这笔交易对公司有什么战略意义？” 　　Leslie Vadasz负责监管英特尔公司的风险资金投向 　　进入九十年代以来，英特尔出于自身的业务特点及电脑业的整体发展态势，把刺激 发展PC市场作为公司的中心投资战略。比如，几年前，英特尔开发了多能奔腾MMX芯片及 基于芯片组的AGP架构。为了推进这些技术的发展，英特尔大力投资像AvidTechnologie s这样的数字影像技术公司。这样，PC彩卡的发展跃上了一个新台阶，Vadas z说：“我 们把视频计算能力推向了一个新高度。” 　　然而，现在英特尔把它的目光投向PC外面的世界，它的投资方向也来了个直转弯。 这家公司在追求一个类似于其P C视频的战略，不过，现在它的注意力集中在网络方面。 这方面的一大举措就是八月份英特尔以20亿美元股票购进了网络芯片生产商Level One Communications。这一购进促进了英特尔所谓Internet Excha ngeArchitecture (IXA) 的网络新战略，IXA指一种用于触发器和路由器的可擦写芯片的生产，为此，英特尔已经 启动了达200,000,000美元的“英特尔通讯基金”（IntelCommunications F und）。 　　这笔基金的首次投入是九月份对Trillium Digital Systems的投资。作为回报，Tr il lium这家通讯软件生产商将优化其产品对IXA芯片的支持。Vadasz 说：“这是第一家 即将利用IXA芯片优势的公司。” 　　英特尔也在向那些支持其设计中的Itanium芯片的公司，Itanium是英特尔全64位处 理器，它瞄准的是高端服务器与工作站市场。为了开发新一代Itanium处理器，英特尔创 立了Intel 64 Fund基金，这包括250,000,000美元风险基金，而这当中包括150,000,00 0美元来自戴尔电脑及Morgan Sta nley Dean Witter的外部资金，这也是英特尔首次向 外融资。Intel 64 Fund基金已经做出了几项投资，这些接受投资的公司大多制造针对I tanium芯片的软件。 　　作为英特尔1968年创建时的元老之一，Vadasz对PC机的持续发展充满信心，他说： “在可预见的将来，我认为PC将成为互联网的主要接入设备。”不过，他也承认PC机市 场正向不同的商业模式分裂，这包括免费PC与专门供互联网接入的单功能廉价电脑。他 说：“这些产品的价格及功能将有较大的差别。” 　　不管未来如何发展，英特尔的投资触角总会指向那里�D�D而且这种导向也许会先于 它的主导产业。Vadasz说： “我们的投资方向就是我们业务战略的风向舵，在许多方面 ，它就是新技术的一扇窗口。”（CPCW专稿） -- 见了mm就灵感大发 港台歌曲唱的全是废话"
# Map data into vocabulary
vocab_path = os.path.join(FLAGS.checkpoint_dir, "..", "vocab")
vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)

x_test = np.array(list(vocab_processor.transform( x_raw )))

with graph.as_default():
    session_conf = tf.ConfigProto(
    allow_soft_placement=FLAGS.allow_soft_placement,
    log_device_placement=FLAGS.log_device_placement)
    sess = tf.Session(config=session_conf)
    with sess.as_default():
        # 初始化变量：全局和局部
        init = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
        sess.run(init)
        
        saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
        saver.restore(sess, checkpoint_file)
        # Get the placeholders from the graph by name
        input_x = graph.get_operation_by_name("input_x").outputs[0]
        # input_y = graph.get_operation_by_name("input_y").outputs[0]
        dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

        # Tensors we want to evaluate
        predictions = graph.get_operation_by_name("output/predictions").outputs[0]
        # 测试：打印 20 个预测值 和 真实值 的对
        # test_output = sess.run(logits, {input_x: test_x[:20]})
        test_output = sess.run(predictions, {input_x: x_test, dropout_keep_prob: 1.0}) 
        print(test_output, 'Inferenced numbers')  # 推测的数字 
