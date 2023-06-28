docker build -t odinluo/xunfei2ui .
docker push odinluo/xunfei2ui
docker save -o xunfei2ui.tar odinluo/xunfei2ui:latest
move xunfei2ui.tar \\10.0.0.1\docker\images