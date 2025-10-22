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
pip list | grep "qwen"
pip list | grep "llava"
pip list | grep "vllm"
pip list | grep "swift"
pip list | grep "attn"
pip list | grep "transformers"
pip list | grep "langchain"
echo

echo "-------------mmdetection/mmseg---------------"
pip list | grep "mm"
echo

echo "-------------sam---------------"
pip list | grep "sam"
pip list | grep "anything"
echo






