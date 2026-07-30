echo
python --version
echo

nvcc --version
echo


echo "-------------torch---------------"
pip list | grep "torch"
echo

echo "-------------onnx---------------"
pip list | grep "onnx"
echo

echo "-------------agent---------------"
pip list | grep -E "qwen|llava|vllm|swift|attn|transformers|langchain|lmdeploy"
echo

echo "-------------mmdetection/mmseg---------------"
pip list | grep "mm"
echo

echo "-------------sam---------------"
pip list | grep -E "sam|anything"
echo