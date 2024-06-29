INPUT_DIR='input'
OUTPUT_DIR='output'
EXPECTED_OUTPUT_DIR='expected_output'

OLD_OUTPUT_PATH=$OUTPUT_PATH

#!/bin/bash
echo '$INPUT_DIR/input_a.txt'
cat $INPUT_DIR/input_a.txt | python3 main.py
mv $OUTPUT_PATH $OUTPUT_DIR/output_a.txt
diff $OUTPUT_DIR/output_a.txt $EXPECTED_OUTPUT_DIR/expected_output_a.txt || echo 'FAIL'

echo ''
echo '$INPUT_DIR/input_0.txt'
cat $INPUT_DIR/input_0.txt | python3 main.py
mv $OUTPUT_PATH $OUTPUT_DIR/output_0.txt
diff $OUTPUT_DIR/output_0.txt $EXPECTED_OUTPUT_DIR/expected_output_0.txt || echo 'FAIL'

echo ''
echo '$INPUT_DIR/input_1.txt'
cat $INPUT_DIR/input_1.txt | python3 main.py
mv $OUTPUT_PATH $OUTPUT_DIR/output_1.txt
diff $OUTPUT_DIR/output_1.txt $EXPECTED_OUTPUT_DIR/expected_output_1.txt || echo 'FAIL'

echo ''
echo '$INPUT_DIR/input_2.txt'
cat $INPUT_DIR/input_2.txt | python3 main.py
mv $OUTPUT_PATH $OUTPUT_DIR/output_2.txt
diff $OUTPUT_DIR/output_2.txt $EXPECTED_OUTPUT_DIR/expected_output_2.txt || echo 'FAIL'

echo ''
echo '$INPUT_DIR/input_3.txt'
cat $INPUT_DIR/input_3.txt | python3 main.py
mv $OUTPUT_PATH $OUTPUT_DIR/output_3.txt
diff $OUTPUT_DIR/output_3.txt $EXPECTED_OUTPUT_DIR/expected_output_3.txt || echo 'FAIL'

echo ''
echo '$INPUT_DIR/input_4.txt'
cat $INPUT_DIR/input_4.txt | python3 main.py
mv $OUTPUT_PATH $OUTPUT_DIR/output_4.txt
diff $OUTPUT_DIR/output_4.txt $EXPECTED_OUTPUT_DIR/expected_output_4.txt || echo 'FAIL'

echo ''
echo '$INPUT_DIR/input_4_2.txt'
cat $INPUT_DIR/input_4_2.txt | python3 main.py
mv $OUTPUT_PATH $OUTPUT_DIR/output_4_2.txt
diff $OUTPUT_DIR/output_4_2.txt $EXPECTED_OUTPUT_DIR/expected_output_4_2.txt || echo 'FAIL'

echo ''
echo '$INPUT_DIR/input_5.txt'
cat $INPUT_DIR/input_5.txt | python3 main.py
mv $OUTPUT_PATH $OUTPUT_DIR/output_5.txt
diff $OUTPUT_DIR/output_5.txt $EXPECTED_OUTPUT_DIR/expected_output_5.txt || echo 'FAIL'

export OUTPUT_PATH=$OLD_OUTPUT_PATH
