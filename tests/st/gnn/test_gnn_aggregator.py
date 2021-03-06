# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""test gnn aggregator."""
import numpy as np

import mindspore.nn as nn
import mindspore.context as context
from mindspore import Tensor
from mindspore.common.api import _executor
import mindspore.ops.composite as C
from aggregator import MeanAggregator

context.set_context(mode=context.GRAPH_MODE)


class MeanAggregatorGrad(nn.Cell):
    """Backward of MeanAggregator"""
    def __init__(self, network):
        super(MeanAggregatorGrad, self).__init__()
        self.grad_op = C.grad_all_with_sens
        self.network = network

    def construct(self, x, sens):
        grad_op = self.grad_op(self.network)(x, sens)
        return grad_op


def test_MeanAggregator():
    """Compile MeanAggregator forward graph"""
    aggregator = MeanAggregator(32, 64, activation="relu", dropout_ratio=0.5)
    input_data = Tensor(np.array(np.random.rand(32, 3, 32), dtype=np.float32))
    _executor.compile(aggregator, input_data)


def test_MeanAggregator_grad():
    """Compile MeanAggregator backward graph"""
    aggregator = MeanAggregator(32, 64, activation="relu", dropout_ratio=0.5)
    input_data = Tensor(np.array(np.random.rand(32, 3, 32), dtype=np.float32))
    sens = Tensor(np.ones([32, 64]).astype(np.float32))
    grad_op = MeanAggregatorGrad(aggregator)
    _executor.compile(grad_op, input_data, sens)
