// Copyright © 2026 Christopher Snow

import { PageConfig } from "@jupyterlab/coreutils";
import { ServiceWorkerManager, IServiceWorkerManager } from "@jupyterlite/apputils";
import { IKernelClient } from "@jupyterlite/services";

// JupyterLite 0.8.6's version-change method unregisters every worker on the origin, including
// other GitHub Pages projects. Let the browser update registrations normally instead. Keeping
// its manager preserves the upstream contents and stdin bridge, including offline Python I/O.
class CourseWorkerManager extends ServiceWorkerManager {
  async _unregisterOldServiceWorkers() {}
}

export const courseWorker = {
  id: "ms-notebook-buttons:service-worker",
  autoStart: true,
  provides: IServiceWorkerManager,
  optional: [IKernelClient],
  activate(app, kernels) {
    const configured = PageConfig.getOption("msOfflineWorker");
    const workerUrl = configured
      ? new URL(configured, new URL(PageConfig.getBaseUrl(), window.location.href)).href
      : undefined;
    const manager = new CourseWorkerManager({ contents: app.serviceManager.contents, workerUrl });
    if (kernels) manager.registerStdinHandler("kernel", kernels.handleStdin.bind(kernels));
    return manager;
  },
};
