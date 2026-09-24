# Module 4 – Introduction to Recurrent Neural Networks (RNN)
> Week 6 · Deep Learning   |   ⬅ Previous: [Module 3 – Introduction to CNN](../Module_3_Introduction_to_CNN)  ·  Next ➡: [Module 5 – Model Performance Metrics](../Module_5_Model_Performance_Metrics)

## 🎯 Learning Objectives
- Understand why sequences (time series, text) need a model with **memory**.
- Implement an RNN cell's forward pass from scratch.
- Understand the **vanishing gradient** problem and how the LSTM's gates solve it.
- Train and compare Keras `SimpleRNN` and `LSTM` on a forecasting task.

## ✅ Syllabus Checklist
- [x] Introduction to RNN
- [x] Introduction to LSTM
- [x] RNN vs LSTM

## 📖 Concepts

### Recurrent Neural Networks
Dense and CNN models see each input on its own. An RNN reads a **sequence** one step at a time and carries a hidden state $h_t$, its "memory":
$$ h_t = \tanh(W_x x_t + W_h h_{t-1} + b), \qquad y_t = W_y h_t + b_y $$
The **same weights** are reused at every time step ("unrolled" through time):
```
x0 ─►[RNN]─h0─►[RNN]─h1─►[RNN]─h2─► ... ─► y
          ▲         ▲         ▲
          x0        x1        x2
```
Uses include stock prices, weather, sensor data, text, speech and music.

### The vanishing gradient problem
Training uses *backpropagation through time*. The gradient that reaches step $t$ is a product of one Jacobian per step:
$$ \frac{\partial h_T}{\partial h_t} = \prod_{k=t+1}^{T} \operatorname{diag}(1-h_k^2)\, W_h $$
If those factors are below 1, the product shrinks **exponentially**. In our demo it falls from 4 to about $10^{-8}$ over 50 steps. If they are above 1, it explodes. So a plain RNN effectively forgets anything more than about 10 to 20 steps back.

### LSTM – Long Short-Term Memory
The LSTM adds a separate **cell state** $c_t$ (a "conveyor belt") that is changed only through **gates** (sigmoids between 0 and 1):
| Gate | Question it answers |
|---|---|
| Forget gate $f_t$ | What old memory should I erase? |
| Input gate $i_t$ + candidate $\tilde c_t$ | What new information should I store? |
| Output gate $o_t$ | What part of memory should I output now? |

$$ c_t = f_t \odot c_{t-1} + i_t \odot \tilde c_t, \qquad h_t = o_t \odot \tanh(c_t) $$
Because $c_t$ is updated by **addition** (not repeated matrix multiplication), gradients can flow across long distances.

### RNN vs LSTM
| | SimpleRNN | LSTM |
|---|---|---|
| Memory | Hidden state only | Hidden state + gated cell state |
| Long-range dependencies | Poor (vanishing gradient) | Good |
| Parameters (32 units, 1 input) | 1,121 | 4,385 (about 4×) |
| Speed | Faster | Slower |
| When to use | Short sequences, quick baselines | Long sequences, text, most real tasks |
| Related | – | GRU: 2 gates, a lighter LSTM alternative |

### Our experiment (synthetic data)
Signal: `sin(t) + 0.5·sin(t/3) + noise` (seeded, **synthetic**). Input: the previous 40 values. Target: the next value. Split: first 80% train / last 20% test (**no shuffling**, because time order matters).

| Model | Params | Train time | Test MSE |
|---|---|---|---|
| SimpleRNN(32) | 1,121 | ~2.7 s | 0.0046 |
| LSTM(32) | 4,385 | ~4.1 s | 0.0046 |
| Naive "next = last" | 0 | – | 0.0107 |

Both models more than halve the naive baseline's error. On a smooth wave that only needs **short** memory they perform about the same. The LSTM's advantage shows when the target depends on inputs far back in the sequence (long texts, long-range seasonality). Honest results like this matter: a bigger model is not automatically better.

## 📂 Files in this Module
| File | What it demonstrates |
|---|---|
| `01_rnn_cell_from_scratch.py` | NumPy RNN cell forward pass (watch the memory of one input spike fade), then the vanishing-gradient curve $\lVert\partial h_T/\partial h_t\rVert$ for three weight scales |
| `02_simplernn_vs_lstm_sine.py` | Keras `SimpleRNN` vs `LSTM` on synthetic sine-wave forecasting, with a comparison table, validation curves and a forecast plot |

## ▶️ How to Run
```bash
cd Week_6_Deep_Learning/Module_4_Introduction_to_RNN
python 01_rnn_cell_from_scratch.py
python 02_simplernn_vs_lstm_sine.py                 # --epochs 10 --window 40
python 02_simplernn_vs_lstm_sine.py --epochs 30 --window 80
```

## 🧠 Key Takeaways
- RNNs share weights across time and carry a hidden state, so they suit sequential data.
- Plain RNNs suffer from vanishing (or exploding) gradients, which limits their memory.
- LSTMs add a gated cell state updated by addition, which keeps long-term memory at about 4× the parameters.
- For time series: create sliding windows, split **chronologically**, and always compare against a naive baseline.

## 📝 Practice Exercises
1. In `01_rnn_cell_from_scratch.py`, replace `tanh` with ReLU and see what happens to the gradient norms (exploding?).
2. Add a `keras.layers.GRU(32)` model to the comparison in `02_simplernn_vs_lstm_sine.py`.
3. Build a task that *needs* long memory. For example, the target is the value 100 steps back: `y = series[i]` for window `series[i:i+120]`. Compare SimpleRNN and LSTM.
4. Stack two LSTM layers (`LSTM(32, return_sequences=True)` then `LSTM(16)`) and compare the MSE.
5. Forecast 10 steps ahead recursively by feeding each prediction back in as input.
