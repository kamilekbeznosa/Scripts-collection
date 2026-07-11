import logging
from kubernetes import client, config

logger = logging.getLogger(__name__)


def check_cluster_health(namespace: str = "default"):
    try:
        config.load_kube_config()
        logger.info("Używam lokalnego kontekstu kubeconfig")
    except Exception:
        try:
            config.load_incluster_config()
            logger.info("Używam ServiceAccount wewnątrz klastra")
        except Exception:
            logger.error("Nie udało się połączyć z klastrem (ani lokalnie, ani wewnątrz)")
            return True
    v1 = client.CoreV1Api()
    logger.info(f"Skanowanie namespace: {namespace}")

    pods = v1.list_namespaced_pod(namespace)
    has_critical = False

    for pod in pods.items:
        status = pod.status.phase
        if status in ["Failed", "Unknown"]:
            logger.error(f"[CRITICAL] Pod {pod.metadata.name} jest w stanie {status}")
            has_critical = True

        for container_status in pod.status.container_statuses or []:
            if container_status.state.waiting and container_status.state.waiting.reason in [
                "CrashLoopBackOff",
                "ImagePullBackOff",
            ]:
                logger.error(
                    f"[CRITICAL] Kontener {container_status.name} w Podzie {pod.metadata.name} ma stan {container_status.state.waiting.reason}"
                )
                has_critical = True

    return has_critical
