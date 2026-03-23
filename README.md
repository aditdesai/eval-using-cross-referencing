# **Beyond Accuracy: Toward Human-Cognitive Evaluation of Multimodal Models through Dynamic Cross-Referencing**


# ILLUSTRATION OF PERTURBED SAMPLES GENERATED FOR FUNCTIONS/GRAPHS

## IMAGE ONLY MODALITY USED (Answer-preserving Perturbation in Images)

<table align='center'>

<tr>
<th>Original Image</th>
<th>Perturbed Image</th>
<th>Perturbed Image</th>
</tr>
  
<tr>
  <td align = "center"><img src="https://github.com/user-attachments/assets/f247bad5-1df0-4a44-b4f9-14d6e10e2a71" width="300"/></td>
<td align = "center"><img src="https://github.com/user-attachments/assets/77f1550b-2fc2-442d-b1fc-635b5cba6129" width="300"/><br> Noise = Grids + Dashed Line</td>
<td align = "center"><img src="https://github.com/user-attachments/assets/243be985-4a5c-455f-88a3-9a3026ba3260" width="300"/><br> Noise = Redundant Dimension </td>
</tr>
</table>


## TEXT ONLY MODALITY USED (Answer-preserving Perturbation in Texts)

<table align='center'>

<tr>
<th>Original Question</th>
<th>Perturbed Question</th>
</tr>

<tr>
<td align='center'>There are two points at -2 and 1 on the number line. Write the set of numbers represented on the number line in interval notation.</td>
<td align='center'>There are two points at -2 and 1 on the number line. The teacher wrote this on the board.  Write the set of numbers represented on the number line in interval notation. John was thinking about lunch.</td>
</tr>

<tr>
<td align='center'>There is a point at 4 and a blue arrow goes to left from that point. Write the set of numbers represented on the number line in interval notation.</td>
<td align='center'>There is a point at 4 and a blue arrow goes to left from that point. [Page 1814] Write the set of numbers represented on the number line in interval notation.</td>
</tr>
</table>


## TEXT + IMAGE MODALITY USED (Answer-Disturbing Perturbation in Either Modality)

<table align='center'>

<tr>
<th>Original Text + Original Image</th>
<th>Original Text + Perturbed Image</th>
<th>Perturbed Text + Original Image</th>
</tr>

<tr>
  <td align = "center">There is an ellipse, for which the domain is from -3 to -1 and the range is from -1 to 3. Determine if this relation is a one-to-one function.</td>
  <td align = "center">There is an ellipse, for which the domain is from -3 to -1 and the range is from -1 to 3. Determine if this relation is a one-to-one function.</td>
  <td align = "center">There is an ellipse, for which the domain is from -3 to -1 and the range is from -I to 3. Determine if this relation is a one-to-one function.</td>
</tr>

<tr>
  <td align = "center"><img src="https://github.com/user-attachments/assets/e2708b6e-d18b-4bed-a779-8e5c115b3579" width = "300"/></td>
  <td align = "center"><img src="https://github.com/user-attachments/assets/24a8bf1f-2efb-4820-8c88-6dfcf73923b3" width = "300"/></td>
  <td align = "center"><img src="https://github.com/user-attachments/assets/e2708b6e-d18b-4bed-a779-8e5c115b3579" width = "300"/></td>
</tr>
</table>


## TEXT + IMAGE MODALITY USED (Answer-Preserving Perturbation in Either Modality)

<table align='center'>

<tr>
<th>Original Text + Original Image</th>
<th>Original Text + Perturbed Image</th>
<th>Perturbed Text + Original Image</th>
</tr>

<tr>
  <td align = "center">There is an ellipse, for which the domain is from -3 to -1 and the range is from -1 to 3. Determine if this relation is a one-to-one function.</td>
  <td align = "center">There is an ellipse, for which the domain is from -3 to -1 and the range is from -1 to 3. Determine if this relation is a one-to-one function.</td>
  <td align = "center">There is an ellipse, for which the domain is from -3 to -1 and the range ID:1738 is from -1 to 3. Determine if this relation is a one-to-one function.</td>
</tr>

<tr>
  <td align = "center"><img src="https://github.com/user-attachments/assets/e2708b6e-d18b-4bed-a779-8e5c115b3579" width = "300"/></td>
  <td align = "center"><img src="https://github.com/user-attachments/assets/464d32fc-8507-4557-a0f8-998f34a548f5" width = "300"/></td>
  <td align = "center"><img src="https://github.com/user-attachments/assets/e2708b6e-d18b-4bed-a779-8e5c115b3579" width = "300"/></td>
</tr>
</table>

# CASE STUDY

<table align = "centre">
  <tr>
    <th>Configuration</th>
    <th>Inputs</th>
    <th>Reasoning By Gemma 3 4B</th>
    <th>Reasoning By Mistral Small 3.2 24B</th>
    <th>Reasoning By Llama 4 Scout 109B</th>
  </tr>
  <tr>
    <td align = "center">Answer Disturbing Text + Original Image</td>
    <td align = "center">There is a piecewise function combind by straight lines going through (3, -2), (1, O), and (O,I). Write an equation for the graphed function f. <br>
      <img src="https://github.com/user-attachments/assets/41ab1449-291f-4b48-986d-01cd45dedf22" width = "150"/>
    </td>
    <td align = "center">
      Okay, let's break down this piecewise function problem.

**1. Identify the Line Segments**

From the graph, we can see the function is made up of two line segments:

*   **Segment 1:** Passes through the points (3, -2) and (1, 0).
*   **Segment 2:** Passes through the points (1, 0) and (0, 1).

**2. Find the Equations of the Lines**

*   **Segment 1: (3, -2) and (1, 0)**

    *   **Slope (m):**  (y2 - y1) / (x2 - x1) = (0 - (-2)) / (1 - 3) = 2 / -2 = -1
    *   Using the point-slope form (y - y1) = m(x - x1) with the point (1, 0):
        y - 0 = -1(x - 1)
        y = -x + 1

*   **Segment 2: (1, 0) and (0, 1)**

    *   **Slope (m):** (y2 - y1) / (x2 - x1) = (1 - 0) / (0 - 1) = 1 / -1 = -1
    *   Using the point-slope form with the point (1, 0):
        y - 0 = -1(x - 1)
        y = -x + 1

**3. Write the Piecewise Function**

Now we can write the piecewise function as:

f(x) =  { -x + 1,  if x ≤ 1
         { -x + 1,  if x > 1

**Important Note:**  The graph shows that the two line segments are the same.  The equation is the same for both segments.

**Final Answer:**

f(x) = -x + 1
    </td>
    <td align = "center">
    To find the equation of the piecewise function \( f \), we need to determine the equations of the individual line segments that make up the function. The given points are (3, -2), (1, 0), and (0, 1).

1. **Determine the equation of the line segment from (0, 1) to (1, 0):**

   - Slope (\( m \)) calculation:
     \[
     m = \frac{y_2 - y_1}{x_2 - x_1} = \frac{0 - 1}{1 - 0} = \frac{-1}{1} = -1
     \]

   - Using the point-slope form \( y - y_1 = m(x - x_1) \) with point (0, 1):
     \[
     y - 1 = -1(x - 0) \implies y = -x + 1
     \]

2. **Determine the equation of the line segment from (1, 0) to (3, -2):**

   - Slope (\( m \)) calculation:
     \[
     m = \frac{y_2 - y_1}{x_2 - x_1} = \frac{-2 - 0}{3 - 1} = \frac{-2}{2} = -1
     \]

   - Using the point-slope form \( y - y_1 = m(x - x_1) \) with point (1, 0):
     \[
     y - 0 = -1(x - 1) \implies y = -x + 1
     \]

3. **Combine the equations:**

   Since both line segments have the same slope and y-intercept, the equation of the function \( f \) is:
   \[
   f(x) = -x + 1
   \]

Thus, the equation for the graphed function \( f \) is:
\[
f(x) = -x + 1
\]
    </td>
    <td align = "center">
    **Problem Statement**

The problem asks us to write an equation for the graphed function f.

**Step 1: Analyzing the Graph**

The graph provided is a piecewise function composed of straight lines. It passes through the points (-3, -2), (0, 1), and (-1, 0).

**Step 2: Identifying the Function's Behavior**

To determine the equation of the function, we need to analyze its behavior in different intervals.

*   For $x < -3$, the graph is a straight line with a positive slope.
*   For $-3 \leq x < -1$, the graph is a straight line with a negative slope.
*   For $x \geq -1$, the graph is a straight line with a positive slope.

**Step 3: Finding the Equation of Each Line Segment**

Let's find the equations of each line segment:

*   **Line Segment 1 ($x < -3$):**
    *   The slope of this line can be calculated using two points on the line, such as (-4, -1) and (-5, 0). The slope is $\frac{0 - (-1)}{-5 - (-4)} = -1$.
    *   Using the point-slope form with (-4, -1), we get $y - (-1) = -1(x - (-4))$, which simplifies to $y = -x - 5$.
*   **Line Segment 2 ($-3 \leq x < -1$):**
    *   The slope of this line can be calculated using the points (-3, -2) and (-1, 0). The slope is $\frac{0 - (-2)}{-1 - (-3)} = 1$.
    *   Using the point-slope form with (-3, -2), we get $y - (-2) = 1(x - (-3))$, which simplifies to $y = x + 1$.
*   **Line Segment 3 ($x \geq -1$):**
    *   The slope of this line can be calculated using the points (-1, 0) and (0, 1). The slope is $\frac{1 - 0}{0 - (-1)} = 1$.
    *   Using the point-slope form with (-1, 0), we get $y - 0 = 1(x - (-1))$, which simplifies to $y = x + 1$.

**Step 4: Writing the Piecewise Function**

Based on the analysis, the piecewise function representing the graph is:

$f(x) = \begin{cases} 
-x - 5 & \text{if } x < -3 \\
x + 1 & \text{if } x \geq -3 
\end{cases}$

**Conclusion**

The equation for the graphed function f is $f(x) = |x + 1|$ for $x \geq -3$ and $f(x) = -x - 5$ for $x < -3$. However, since the graph is continuous at $x = -3$, we can simplify it to $f(x) = |x + 1|$ for all $x$. Therefore, the final answer is $f(x) = |x + 1|$.
    </td>
  </tr>
</table>


