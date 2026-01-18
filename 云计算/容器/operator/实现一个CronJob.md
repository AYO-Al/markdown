
# 

每组 `Controllers` 都需要一个 `Scheme` 。它提供了 Kinds 与 Go 类型之间的映射。

```go
var (
    scheme   = runtime.NewScheme()
    setupLog = ctrl.Log.WithName("setup")
)

func init() {
    utilruntime.Must(clientgoscheme.AddToScheme(scheme))

    // +kubebuilder:scaffold:scheme
}

```
