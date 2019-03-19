# 
# model visualize module
# author: topol @ USTC
# last modified: 2019/3/19
#
from IPython.display import Image
from sklearn import tree
import pydotplus

def dt_viz(dtc, feature):
    # 决策树可视化输出
    dt_file = "./model/dt.dot"
    with open(dt_file,"w") as f:
        # tree.export_graphviz(dtc, feature_names=vec.get_feature_names(), out_file = f)
        dot_data = tree.export_graphviz(dtc, feature_names=feature, out_file = f, \
            filled=True, rounded=True, special_characters=True)
        
        # 这里直接画图有点问题
        # 可能要用绝对路径
        # 在src下输入 dot -Tpng ./model/dt.dot -o ./model/dt.png 即可得到可视化结果
        # dt_png = "./model/tree.png"
        # command = ["dot", "-Tpng", dt_file, "-o", dt_png]
        # command = " ".join(command)
        # try:
        #     subprocess.check_call(command, shell=True)
        # except Exception as e:
        #     print(e)
        #     exit("Could not run dot, ie graphviz, to "
        #          "produce visualization")
    print("dt.dot saved in ./model!")

def rf_viz(rfc, feature):
    # 随机森林可视化输出
    Estimators = rfc.estimators_
    for index, model in enumerate(Estimators):
        filename = './model/rf_viz/rf_' + str(index) + '.pdf'
        dot_data = tree.export_graphviz(model , out_file=None,
                            feature_names=feature,
                            filled=True, rounded=True,
                            special_characters=True)
        graph = pydotplus.graph_from_dot_data(dot_data)
        Image(graph.create_png())
        graph.write_pdf(filename)
    print("rf.png saved in ./model/rf_viz!")