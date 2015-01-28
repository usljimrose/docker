from fabric.api import env, task
from envassert import detect, file, package, process, service


@task
def check():
    env.platform_family = detect.detect()

    assert package.installed("lxc-docker")
    assert file.exists("/etc/default/docker")
    assert file.exists("/var/run/docker.sock")
    assert process.is_up("docker")
    assert service.is_enabled("docker")


@task
def artifacts():
    env.platform_family = detect.detect()

    # Logs to pull
    logs = ['/root/cfn-userdata.log',
            '/root/heat-script.log',
            '/tmp/heat_chef/chef-stacktrace.out']

    # Artifacts target location
    try:
        os.environ['CIRCLE_ARTIFACTS']
    except:
        artifacts = 'tmp'
    else:
        artifacts = os.environ['CIRCLE_ARTIFACTS']

    # For each log, get it down
    for log in logs:
        target = artifacts + "/%(host)s/%(path)s"
        get(log, target)
