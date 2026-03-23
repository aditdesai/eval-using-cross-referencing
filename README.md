# eval-using-cross-referencing
KDD BlueSky Submission titled "Beyond Accuracy: Toward Human-Cognitive Evaluation of Multimodal Models through Dynamic Cross-Referencing"


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


